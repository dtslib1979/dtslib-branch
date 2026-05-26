#!/usr/bin/env python3
"""
FLD OS → Phone MCP Bridge
SSH로 폰 MCP Distributor에 연결하여 도구 호출

폰 MCP 도구:
  parksy_distribute_telegram(mp4_path, caption, chat_id?)
  parksy_distribute_telegram_photo(img_path, caption?, chat_id?)
  parksy_distribute_telegram_text(text, chat_id?)
  parksy_distribute_youtube(mp4_path, title, description, ...)
  parksy_distribute_naver(account, title, content, tags?)
  parksy_distribute_tistory(account, blog, title, content_html, ...)
  parksy_distribute_discord(mp4_path|message, webhook_url?)
  parksy_distribute_all(content_spec)
  parksy_distribute_status()
  parksy_distribute_list_channels(platform?)
  parksy_distribute_refresh_tokens(account?)
"""
import json, os, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── 설정 ───
PHONE_IP = os.environ.get("PHONE_IP", "")
PHONE_SSH_PORT = int(os.environ.get("PHONE_SSH_PORT", "8022"))
PHONE_USER = os.environ.get("PHONE_USER", "")
MCP_SERVER_PATH = "/data/data/com.termux/files/home/mcp_server.py"
FLD_OS_DIR = Path(os.environ.get("FLD_OS_DIR", str(Path.home() / "dtslib-branch" / "fld-os")))

# SSH 기본 옵션
SSH_OPTS = [
    "-p", str(PHONE_SSH_PORT),
    "-o", "ConnectTimeout=10",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ServerAliveInterval=15",
]

def _ssh_target() -> str:
    """SSH 대상 문자열"""
    if PHONE_USER:
        return f"{PHONE_USER}@{PHONE_IP}"
    return PHONE_IP


def call_mcp_tool(tool_name: str, params: dict = None, timeout: int = 60) -> dict:
    """
    폰 MCP Distributor의 도구를 SSH로 호출.
    MCP Distributor에 stdin으로 JSON-RPC 요청을 보냄.
    """
    if not PHONE_IP:
        # IP 자동 탐색
        try:
            result = subprocess.run(
                ["tailscale", "status"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if "s25-ultra" in line.lower():
                    PHONE_IP_auto = line.split()[0]
                    os.environ["PHONE_IP"] = PHONE_IP_auto
                    print(f"  → Phone IP auto-detected: {PHONE_IP_auto}")
                    return call_mcp_tool(tool_name, params, timeout)
        except Exception:
            pass
        return {"error": "PHONE_IP not set. Set PHONE_IP env or ensure tailscale running."}

    if params is None:
        params = {}

    # JSON-RPC 요청 구성
    rpc_request = {
        "jsonrpc": "2.0",
        "id": str(int(time.time() * 1000)),
        "method": f"tools/call",
        "params": {
            "name": tool_name,
            "arguments": params,
        }
    }

    # 임시 Python 스크립트 생성 (MCP 클라이언트)
    script = f'''#!/usr/bin/env python3
import json, sys, os
sys.path.insert(0, "{MCP_SERVER_PATH}")
# FastMCP 서버 인스턴스 직접 호출
import importlib.util
spec = importlib.util.spec_from_file_location("mcp_server", "{MCP_SERVER_PATH}")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# 도구 조회
tool_fn = getattr(mod, "{tool_name}", None)
if not tool_fn:
    # @mcp.tool() 데코레이터로 등록된 함수 찾기
    for name in dir(mod):
        if name.startswith("parksy_") and callable(getattr(mod, name)):
            tool_fn = getattr(mod, name)
            break

if not tool_fn:
    print(json.dumps({{"error": "Tool {{tool_name}} not found"}}, ensure_ascii=False))
    sys.exit(1)

# 새 MCP 서버 인스턴스로 도구 호출
# FastMCP 도구는 @mcp.tool() 데코레이터로 래핑되어 내부적으로 등록됨
# 직접 호출 불가 → 대신 MCP 클라이언트로 invoke

from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
import anyio

async def main():
    server_params = StdioServerParameters(
        command="python3",
        args=["{MCP_SERVER_PATH}"],
    )
    async with stdio_client(server_params) as (read, write):
        from mcp import ClientSession
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("{tool_name}", {json.dumps(params)})
            print(json.dumps({{"result": result.content[0].text if result.content else "no output"}}, ensure_ascii=False))

anyio.run(main)
'''

    # SSH로 Python 스크립트 전송 후 실행
    ssh_cmd = ["ssh"] + SSH_OPTS + [_ssh_target(), "--", "python3", "-c", script]

    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            return {
                "error": f"SSH failed (rc={result.returncode})",
                "stderr": result.stderr[:500],
                "stdout": result.stdout[:500],
            }
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout ({timeout}s) during MCP tool call"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}", "raw": result.stdout[:500]}
    except Exception as e:
        return {"error": str(e)[:200]}


# ─── 고수준 래퍼 ───
def distribute_protocol(fld_item: dict, mp4_path: str = "", protocol_type: str = "telegram") -> dict:
    """FLD Item을 프로토콜 상태로 승격한 후 배포"""
    results = {}

    if protocol_type == "telegram":
        caption = f"📦 {fld_item.get('title', 'FLD Protocol')}\n"
        caption += f"상태: {fld_item.get('state', 'seed')} | 평가: {fld_item.get('score', 0)}/50\n"
        caption += f"계정군: {fld_item.get('account', 'uncategorized')}\n"
        caption += f"ID: {fld_item.get('id', '')}"

        if mp4_path:
            result = call_mcp_tool("parksy_distribute_telegram", {
                "mp4_path": mp4_path,
                "caption": caption,
            })
        else:
            result = call_mcp_tool("parksy_distribute_telegram_text", {
                "text": caption,
            })
        results["telegram"] = result

    elif protocol_type == "youtube":
        result = call_mcp_tool("parksy_distribute_youtube", {
            "mp4_path": mp4_path,
            "title": f"[FLD] {fld_item.get('title', '')[:80]}",
            "description": f"FLD OS Protocol Output\nID: {fld_item.get('id', '')}\n상태: {fld_item.get('state', '')}\n점수: {fld_item.get('score', 0)}/50",
            "channel": fld_item.get("account", "uncategorized"),
        })
        results["youtube"] = result

    elif protocol_type == "all":
        # 전체 채널 배포
        result = call_mcp_tool("parksy_distribute_all", {
            "content_spec": {
                "title": f"[FLD] {fld_item.get('title', '')[:60]}",
                "description": f"FLD OS Protocol: {fld_item.get('id', '')}",
                "mp4_path": mp4_path,
                "account": fld_item.get("account", "uncategorized"),
            }
        })
        results["all"] = result

    return results


def get_distribution_status() -> dict:
    """폰 배포 채널 상태 조회"""
    return call_mcp_tool("parksy_distribute_status")


def list_channels(platform: str = "") -> dict:
    """사용 가능한 채널 목록"""
    return call_mcp_tool("parksy_distribute_list_channels", {"platform": platform})


# ─── CLI ───
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        r = get_distribution_status()
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "channels":
        platform = sys.argv[2] if len(sys.argv) > 2 else ""
        r = list_channels(platform)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "call":
        tool = sys.argv[2] if len(sys.argv) > 2 else ""
        params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        r = call_mcp_tool(tool, params)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "distribute":
        item_id = sys.argv[2] if len(sys.argv) > 2 else ""
        mp4_path = sys.argv[3] if len(sys.argv) > 3 else ""
        ptype = sys.argv[4] if len(sys.argv) > 4 else "telegram"
        # FLD에서 Item 읽기
        fld_ledger = FLD_OS_DIR / "data" / "ledger.jsonl"
        item = None
        if fld_ledger.exists():
            for line in fld_ledger.open():
                d = json.loads(line.strip())
                if d["id"] == item_id:
                    item = d
                    break
        if not item:
            print(json.dumps({"error": f"Item {item_id} not found"}, ensure_ascii=False))
            sys.exit(1)
        r = distribute_protocol(item, mp4_path, ptype)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    else:
        print(f"Usage: {sys.argv[0]} [status|channels|call|distribute]")
