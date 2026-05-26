#!/usr/bin/env python3
"""
FLD OS — Core Ledger Engine
상태: Seed → Scenario → Candidate → Pilot → Protocol
"""
import json, os, re, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── 상태 모델 ───
STATES = ["seed", "scenario", "candidate", "pilot", "protocol"]
STATE_LABELS = {
    "seed": "🌱 Seed (원시 입력)",
    "scenario": "📋 Scenario (장면화)",
    "candidate": "🔍 Candidate (평가 후보)",
    "pilot": "🧪 Pilot (최소 실행)",
    "protocol": "📦 Protocol (자산화)",
}

# ─── 계정군 ───
ACCOUNTS = ["person", "space", "revenue", "channel", "content", "tool", "risk", "asset"]

# ─── 아이템 ───
class FLDItem:
    def __init__(self, title="", raw_source="", actor="", space="", motive="",
                 output_guess="", revenue_guess="", channel="", risk="",
                 next_action="", account="uncategorized"):
        self.id = f"FLD-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at
        self.state = "seed"
        self.title = title
        self.raw_source = raw_source
        self.actor = actor
        self.space = space
        self.motive = motive
        self.output_guess = output_guess
        self.revenue_guess = revenue_guess
        self.channel = channel
        self.risk = risk
        self.next_action = next_action
        self.account = account if account in ACCOUNTS else "uncategorized"
        self.score = 0
        self.score_detail = {}
        self.tags = []
        self.history = [{"state": "seed", "at": self.created_at, "by": "system"}]
        self.links = []  # 연결된 자산 URI
        self.notes = ""
        self.dropped = False
        self.drop_reason = ""

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d):
        obj = cls.__new__(cls)
        for k, v in d.items():
            setattr(obj, k, v)
        return obj


# ─── 장부 엔진 ───
class FLDLedger:
    def __init__(self, path: str = None):
        self.path = path or os.environ.get("FLD_LEDGER_PATH",
            str(Path.home() / "dtslib-branch" / "fld-os" / "data" / "ledger.jsonl"))
        self.items = []
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            for line in open(self.path):
                line = line.strip()
                if line:
                    try:
                        self.items.append(FLDItem.from_dict(json.loads(line)))
                    except json.JSONDecodeError:
                        pass

    def _save(self, item: FLDItem):
        with open(self.path, "a") as f:
            f.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")

    def _rewrite(self):
        with open(self.path, "w") as f:
            for item in self.items:
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")

    # ─── CRUD ───
    def add(self, **kwargs) -> FLDItem:
        item = FLDItem(**kwargs)
        self.items.append(item)
        self._save(item)
        return item

    def get(self, item_id: str) -> Optional[FLDItem]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def update(self, item_id: str, **kwargs) -> Optional[FLDItem]:
        item = self.get(item_id)
        if not item:
            return None
        for k, v in kwargs.items():
            if hasattr(item, k) and k not in ("id", "created_at", "history"):
                setattr(item, k, v)
        item.updated_at = datetime.now(timezone.utc).isoformat()
        self._rewrite()
        return item

    def delete(self, item_id: str) -> bool:
        item = self.get(item_id)
        if not item:
            return False
        self.items = [i for i in self.items if i.id != item_id]
        self._rewrite()
        return True

    # ─── 상태 전이 ───
    def transition(self, item_id: str, to_state: str, by="user") -> Optional[FLDItem]:
        item = self.get(item_id)
        if not item:
            return None
        if to_state not in STATES:
            raise ValueError(f"Invalid state: {to_state}. Must be one of {STATES}")

        current = STATES.index(item.state)
        target = STATES.index(to_state)
        if target < current:
            raise ValueError(f"Cannot regress from {item.state} to {to_state}")

        # 전이 조건 검사
        if to_state == "scenario" and not item.raw_source:
            raise ValueError("Seed→Scenario 실패: raw_source 없음")
        if to_state == "candidate" and not item.account:
            raise ValueError("Scenario→Candidate 실패: 계정군 미분류")
        if to_state == "pilot" and item.score < 30:
            raise ValueError(f"Candidate→Pilot 실패: 점수 {item.score} < 30")
        if to_state == "protocol" and not item.links:
            raise ValueError(f"Pilot→Protocol 실패: 자산 링크 없음")

        item.state = to_state
        item.updated_at = datetime.now(timezone.utc).isoformat()
        item.history.append({"state": to_state, "at": item.updated_at, "by": by})
        self._rewrite()
        return item

    # ─── 점수 평가 ───
    def score_item(self, item_id: str, scores: dict = None) -> Optional[FLDItem]:
        """10개 항목 5점 척도 평가"""
        item = self.get(item_id)
        if not item:
            return None

        if scores is None:
            scores = {}

        criteria = {
            "immediacy": "지금 바로 다음 단계 실행 가능한가",
            "mobile_fit": "모바일에서 입력·검토·실행이 가능한가",
            "log_value": "과정이 장기 자산으로 남는가",
            "reusability": "한 번 만든 뒤 여러 번 쓸 수 있는가",
            "deployability": "GitHub/Pages/APK/PWA/문서로 퍼질 수 있는가",
            "mcp_potential": "규칙이나 툴로 승격 가능한가",
            "revenue_potential": "직간접 경제 흐름을 만들 수 있는가",
            "brand_fit": "Phone-first/박씨 세계관에 맞는가",
            "maintainability": "유지보수 비용이 과도하지 않은가",
            "evidence": "Pilot에서 결과를 회수할 수 있는가",
        }

        total = 0
        detail = {}
        for key, desc in criteria.items():
            score = scores.get(key, 3)  # 기본 3점
            score = max(1, min(5, score))
            detail[key] = {"score": score, "desc": desc}
            total += score

        item.score = total
        item.score_detail = detail
        item.updated_at = datetime.now(timezone.utc).isoformat()
        self._rewrite()
        return item

    # ─── 조회 ───
    def list_by_state(self, state: str) -> list:
        return [i for i in self.items if i.state == state and not i.dropped]

    def list_active(self) -> list:
        return [i for i in self.items if not i.dropped]

    def list_dropped(self) -> list:
        return [i for i in self.items if i.dropped]

    def list_by_account(self, account: str) -> list:
        return [i for i in self.items if i.account == account and not i.dropped]

    def stats(self) -> dict:
        return {
            "total": len(self.items),
            "active": len([i for i in self.items if not i.dropped]),
            "dropped": len([i for i in self.items if i.dropped]),
            "by_state": {s: len(self.list_by_state(s)) for s in STATES},
            "by_account": {a: len(self.list_by_account(a)) for a in ACCOUNTS},
        }

    def export_json(self) -> str:
        return json.dumps([i.to_dict() for i in self.items], ensure_ascii=False, indent=2)

    # ─── Seed 생성: 로그 파일에서 자동 추출 ───
    def ingest_log(self, log_text: str, source_path: str = "") -> FLDItem:
        """Parksy Capture 로그에서 Seed 자동 생성"""
        # 첫 200자에서 제목 추출
        title = log_text.strip()[:80].replace("\n", " ")
        # 화자 분리 시도 (간단)
        user_parts = re.findall(r'(?m)^([A-Z가-힣].+?[.!?])\s*$', log_text[:1000])
        motive = user_parts[0][:200] if user_parts else title[:200]

        item = self.add(
            title=title,
            raw_source=source_path,
            motive=motive,
            next_action="시나리오 검토"
        )
        return item


# ─── 싱글톤 ───
_ledger = None

def get_ledger(path: str = None) -> FLDLedger:
    global _ledger
    if _ledger is None:
        _ledger = FLDLedger(path)
    return _ledger
