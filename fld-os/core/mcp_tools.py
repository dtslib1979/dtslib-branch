#!/usr/bin/env python3
"""
FLD OS — MCP Tool Interface
각 FLD 작업을 MCP-compatible tool로 노출
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ledger import get_ledger, STATES, ACCOUNTS, STATE_LABELS, FLDItem

ledger = get_ledger()

def tool_list():
    """등록된 모든 FLD MCP 툴 목록"""
    return {
        "tools": [
            {"name": "fld_seed", "description": "\U0001f331 새 Seed 생성 (원시 입력)"},
            {"name": "fld_scenario", "description": "\U0001f4cb Seed → Scenario 전환"},
            {"name": "fld_candidate", "description": "\U0001f50d Scenario → Candidate 전환 + 점수 평가"},
            {"name": "fld_pilot", "description": "\U0001f9ea Candidate → Pilot 실행"},
            {"name": "fld_protocol", "description": "\U0001f4e6 Pilot → Protocol 자산화"},
            {"name": "fld_score", "description": "\U0001f4ca 항목 점수 평가 (10항목 5점)"},
            {"name": "fld_list", "description": "\U0001f4cb 상태/계정별 항목 조회"},
            {"name": "fld_stats", "description": "\U0001f4c8 장부 통계"},
            {"name": "fld_ingest", "description": "\U0001f4e5 로그 파일 → Seed 자동 생성"},
            {"name": "fld_drop", "description": "\U0001f5d1️ 항목 폐기"},
        ]
    }

def tool_fld_seed(**kwargs):
    required = ["title", "raw_source"]
    for r in required:
        if r not in kwargs:
            return {"error": f"필수 필드: {r}"}
    item = ledger.add(**kwargs)
    return {"status": "ok", "item": item.to_dict()}

def tool_fld_scenario(item_id: str, **kwargs):
    try:
        item = ledger.transition(item_id, "scenario")
        if not item:
            return {"error": "아이템 없음"}
        return {"status": "ok", "item_id": item_id, "state": "scenario"}
    except ValueError as e:
        return {"error": str(e)}

def tool_fld_candidate(item_id: str, **kwargs):
    try:
        scores = {k: int(v) for k, v in kwargs.items() if k in [
            "immediacy","mobile_fit","log_value","reusability",
            "deployability","mcp_potential","revenue_potential",
            "brand_fit","maintainability","evidence"]}
        ledger.score_item(item_id, scores or None)
        item = ledger.transition(item_id, "candidate")
        if not item:
            return {"error": "아이템 없음"}
        return {"status": "ok", "item_id": item_id, "score": item.score}
    except ValueError as e:
        return {"error": str(e)}

def tool_fld_pilot(item_id: str):
    try:
        item = ledger.transition(item_id, "pilot")
        return {"status": "ok", "item_id": item_id, "state": "pilot"}
    except ValueError as e:
        return {"error": str(e)}

def tool_fld_protocol(item_id: str, asset_links: list = None):
    if asset_links:
        ledger.update(item_id, links=asset_links)
    try:
        item = ledger.transition(item_id, "protocol")
        return {"status": "ok", "item_id": item_id, "state": "protocol"}
    except ValueError as e:
        return {"error": str(e)}

def tool_fld_score(item_id: str, **scores):
    try:
        scores_int = {k: int(v) for k, v in scores.items()}
        item = ledger.score_item(item_id, scores_int)
        if not item:
            return {"error": "아이템 없음"}
        return {"status": "ok", "item_id": item_id, "score": item.score,
                "detail": item.score_detail}
    except ValueError as e:
        return {"error": str(e)}

def tool_fld_list(state: str = "", account: str = ""):
    if state and state in STATES:
        items = ledger.list_by_state(state)
    elif account and account in ACCOUNTS:
        items = ledger.list_by_account(account)
    else:
        items = ledger.list_active()
    return {
        "count": len(items),
        "items": [
            {"id": i.id, "title": i.title[:60], "state": i.state,
             "account": i.account, "score": i.score,
             "created": i.created_at[:10]}
            for i in sorted(items, key=lambda x: x.created_at, reverse=True)
        ]
    }

def tool_fld_stats():
    return ledger.stats()

def tool_fld_ingest(log_text: str = "", source_path: str = ""):
    if not log_text:
        return {"error": "로그 텍스트 필요"}
    item = ledger.ingest_log(log_text, source_path)
    return {"status": "ok", "item": item.to_dict()}

def tool_fld_drop(item_id: str, reason: str = ""):
    item = ledger.get(item_id)
    if not item:
        return {"error": "아이템 없음"}
    item.dropped = True
    item.drop_reason = reason
    ledger._rewrite()
    return {"status": "ok", "item_id": item_id, "dropped": True}

TOOL_MAP = {
    "fld_seed": tool_fld_seed,
    "fld_scenario": tool_fld_scenario,
    "fld_candidate": tool_fld_candidate,
    "fld_pilot": tool_fld_pilot,
    "fld_protocol": tool_fld_protocol,
    "fld_score": tool_fld_score,
    "fld_list": tool_fld_list,
    "fld_stats": tool_fld_stats,
    "fld_ingest": tool_fld_ingest,
    "fld_drop": tool_fld_drop,
}

def handle_mcp_call(tool_name: str, params: dict = None):
    if tool_name == "list_tools":
        return tool_list()
    if tool_name not in TOOL_MAP:
        return {"error": f"Unknown tool: {tool_name}"}
    fn = TOOL_MAP[tool_name]
    if params is None:
        params = {}
    return fn(**params)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        tool = sys.argv[1]
        params = json.loads(sys.argv[2]) if len(sys.argv) >= 3 else {}
        result = handle_mcp_call(tool, params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
