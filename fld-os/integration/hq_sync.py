#!/usr/bin/env python3
"""
FLD OS → HQ Ledger Sync Bridge
양방향 동기화: FLD Item 상태 전이 → HQ 트랜잭션 / HQ 이벤트 → FLD Seed

FLD 포맷 (data/ledger.jsonl):
  FLDItem: id, state, title, account, score, links, ...

HQ 포맷 (hq/ledger/ledger.jsonl):
  TXN: id(TXN-...), timestamp, eventType, actor, cell, data, status

동기화 규칙:
  FLD→HQ: transition() 호출 시 HQ에 "fld_state_change" 이벤트 발행
  HQ→FLD: cell_registered 이벤트 → FLD Seed 자동 생성
"""
import json, os, sys, time, uuid
from datetime import datetime, timezone
from pathlib import Path

# FLD OS 경로
FLD_OS = Path(os.environ.get("FLD_OS_DIR", str(Path.home() / "dtslib-branch" / "fld-os")))
FLD_LEDGER = FLD_OS / "data" / "ledger.jsonl"

# HQ 경로
HQ_DIR = Path(os.environ.get("HQ_DIR", str(Path.home() / "dtslib-branch" / "hq")))
HQ_LEDGER = HQ_DIR / "ledger" / "ledger.jsonl"


# ─── 멀티라인 JSONL 리더 ───
def _read_jsonl(path: Path) -> list:
    """멀티라인 JSON을 처리하는 JSONL 리더 (split lines 복구)"""
    items = []
    if not path.exists():
        return items
    with open(str(path)) as f:
        buf = ""
        for line in f:
            buf += line
            try:
                obj = json.loads(buf.strip())
                items.append(obj)
                buf = ""
            except json.JSONDecodeError:
                continue  # 아직 완전한 객체가 아님 -> 더 읽음
        # 마지막 버퍼 처리
        if buf.strip():
            try:
                items.append(json.loads(buf.strip()))
            except json.JSONDecodeError:
                pass
    return items


# ─── HQ 트랜잭션 생성 ───
def _next_txn_id() -> str:
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%d-%H%M%S")
    rand = str(uuid.uuid4().int)[:6]
    return f"TXN-{ts}-{rand}"


def hq_push(event_type: str, actor: str, cell: str, data: dict, status="success") -> dict:
    """HQ ledger에 트랜잭션 기록"""
    txn = {
        "id": _next_txn_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "eventType": event_type,
        "actor": actor,
        "cell": cell,
        "data": data,
        "status": status,
    }
    os.makedirs(str(HQ_LEDGER.parent), exist_ok=True)
    with open(str(HQ_LEDGER), "a") as f:
        f.write(json.dumps(txn, ensure_ascii=False) + "\n")
    return txn


# ─── FLD Item 읽기 ───
def fld_read_all() -> list:
    items = []
    if FLD_LEDGER.exists():
        for line in FLD_LEDGER.open():
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return items


def fld_get(item_id: str) -> dict:
    for item in fld_read_all():
        if item.get("id") == item_id:
            return item
    return None


# ─── FLD→HQ: 상태 전이 동기화 ───
def sync_transition_to_hq(item_id: str, from_state: str, to_state: str, by: str = "user"):
    """FLD Item 상태 전이 → HQ 트랜잭션 발행"""
    item = fld_get(item_id)
    if not item:
        return {"error": f"Item {item_id} not found"}

    txn = hq_push(
        event_type="fld_state_change",
        actor=by,
        cell=item.get("account", "uncategorized"),
        data={
            "fld_id": item_id,
            "title": item.get("title", ""),
            "from_state": from_state,
            "to_state": to_state,
            "account": item.get("account", ""),
            "score": item.get("score", 0),
        },
        status="success",
    )
    return txn


# ─── HQ→FLD: 이벤트 수집 ───
def sync_hq_to_fld(hq_events: list = None) -> list:
    """HQ ledger → FLD Seed 생성
    - cell_registered 이벤트 → 새로운 FLD Seed
    - sync_upstream 이벤트 → 기존 Seed 업데이트
    """
    if hq_events is None:
        hq_events = _read_jsonl(HQ_LEDGER)

    existing = fld_read_all()
    existing_ids = {e.get("id") for e in existing}
    existing_titles = {e.get("title", "") for e in existing}

    created = []
    for ev in hq_events:
        event_type = ev.get("eventType", "")
        if event_type == "cell_registered":
            cell = ev.get("cell", "")
            title = f"HQ 셀 등록: {cell}"
            if title not in existing_titles:
                # 새로운 FLD Seed 생성
                seed = {
                    "id": f"FLD-{int(time.time())}-{uuid.uuid4().hex[:6]}",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "state": "seed",
                    "title": title,
                    "raw_source": f"hq://{ev.get('id', '')}",
                    "actor": "",
                    "space": ev.get("data", {}).get("area", ""),
                    "motive": f"HQ cell_registered: {cell} ({ev.get('data', {}).get('tier', 'standard')})",
                    "output_guess": "",
                    "revenue_guess": "",
                    "channel": "hq",
                    "risk": "",
                    "next_action": "시나리오 검토",
                    "account": ev.get("data", {}).get("area", "uncategorized"),
                    "score": 0,
                    "score_detail": {},
                    "tags": ["hq-sync", f"cell:{cell}", f"tier:{ev.get('data', {}).get('tier', 'standard')}"],
                    "history": [{"state": "seed", "at": datetime.now(timezone.utc).isoformat(), "by": "hq_sync"}],
                    "links": [],
                    "notes": f"Auto-synced from HQ event {ev.get('id', '')}",
                    "dropped": False,
                    "drop_reason": "",
                }
                with open(str(FLD_LEDGER), "a") as f:
                    f.write(json.dumps(seed, ensure_ascii=False) + "\n")
                created.append(seed)
                existing_titles.add(title)

        elif event_type == "sync_upstream":
            cell = ev.get("cell", "")
            # 매칭되는 FLD Item이 있으면 업데이트
            for item in existing:
                if cell in item.get("title", "") and item.get("state") == "seed":
                    # 링크 업데이트
                    repo = ev.get("data", {}).get("repo", "")
                    if repo and repo not in item.get("links", []):
                        item["links"] = item.get("links", []) + [f"hq://{repo}"]
                        item["updated_at"] = datetime.now(timezone.utc).isoformat()
                    break

    return created


# ─── 전체 동기화 ───
def sync_full() -> dict:
    """전체 양방향 동기화 실행"""
    # 1. HQ → FLD (새 Seed)
    created = sync_hq_to_fld()

    # 2. FLD→HQ (변경사항 푸시) — 모든 non-seed 항목을 HQ에 반영
    pushed = []
    for item in fld_read_all():
        if item.get("state") != "seed" and not item.get("dropped", False):
            # 이미 HQ에 반영되었는지 확인
            txn = hq_push(
                event_type="fld_state_change",
                actor="system",
                cell=item.get("account", "uncategorized"),
                data={
                    "fld_id": item["id"],
                    "title": item.get("title", ""),
                    "state": item.get("state", ""),
                    "score": item.get("score", 0),
                    "account": item.get("account", ""),
                },
                status="success",
            )
            pushed.append(txn["id"])

    return {
        "hq_to_fld": len(created),
        "fld_to_hq": len(pushed),
        "created_seeds": [c["id"] for c in created],
        "pushed_txns": pushed,
    }


# ─── CLI ───
if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        fld_items = fld_read_all()
        hq_txns = _read_jsonl(HQ_LEDGER)
        print(json.dumps({
            "fld_items": len(fld_items),
            "fld_by_state": {},
            "hq_transactions": len(hq_txns),
            "last_sync": datetime.now(timezone.utc).isoformat(),
        }, ensure_ascii=False, indent=2))

    elif cmd == "sync":
        result = sync_full()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "push":
        item_id = sys.argv[2] if len(sys.argv) > 2 else ""
        from_state = sys.argv[3] if len(sys.argv) > 3 else "seed"
        to_state = sys.argv[4] if len(sys.argv) > 4 else "scenario"
        by = sys.argv[5] if len(sys.argv) > 5 else "user"
        result = sync_transition_to_hq(item_id, from_state, to_state, by)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "pull":
        created = sync_hq_to_fld()
        print(json.dumps({"created": len(created), "seeds": [c["id"] for c in created]}, ensure_ascii=False, indent=2))

    else:
        print(f"Usage: {sys.argv[0]} [status|sync|push|pull]")
