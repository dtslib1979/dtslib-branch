#!/usr/bin/env python3
"""
server.py — Φ-I-C-K-P-7AXIS 정치 MCP v0.2 (보좌관 B2B)

형(Claude) 카운터 #003 반영:
  ❌ 6개 툴 중 5개가 일반 LLM 래퍼였음 → 전면 폐기
  ✅ 모든 툴이 Φ7 7축을 통과하는 데이터 기반 분석
  ❌ 타겟: 일반 시민
  ✅ 타겟: 다른 의원실 보좌관 (B2B)

툴 (전부 Φ7 7축 기반):
  1. phi7_profile  — 정치인 7축 프로필 (Core)
  2. phi7_cross    — 두 정치인 7축 비교 매트릭스
  3. phi7_policy   — 정책의 7축 영향 예측
  4. phi7_strategy — 7축 기반 전략 리포트
  5. orchestrate   — ★ 메타: 방법론

사용법:
  echo '{"tool":"phi7_profile","params":{"politician":"park_chan_dae"}}' | python3 server.py
"""

import sys, json, asyncio, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from phi7_political import phi7_profile, phi7_cross, phi7_policy_impact, phi7_strategy, PHI7_LABELS, POLITICIANS

VERSION = "0.2.0"
MCP_NAME = "parksy_political_phi7"

# ─── 메타 툴 ─────────────────────────────────────────────
def make_orchestrate() -> dict:
    """툴 5: 메타 — 방법론 전체 구조"""
    return {
        "tool": "orchestrate",
        "version": VERSION,
        "name": "Φ-I-C-K-P-7AXIS 정치 분석 MCP",
        "description": (
            "시민 1인이 AI 에이전트를 오케스트레이션해서 "
            "정치인 분석 프레임(Φ7 7축)을 만들고, "
            "이를 MCP로 배포하여 다른 의원실 보좌관이 "
            "B2B로 사용하는 도구"
        ),
        "architecture": {
            "method": "일인 오케스트레이션 에이전트 협업",
            "agents": {
                "박씨": "방향 설정·판단",
                "Perplexity": "구조화·논리 검증",
                "DeepSeek": "MCP 구현",
                "Claude": "카운터·설계 검증"
            },
            "flow": "OrbitPrompt(Φ드라이버) → dtslib-branch(정치 MCP) → 현실(보좌관 B2B)",
            "delivery": "GitHub 공개 → 보좌관이 각 의원 맞춤 사용 (역방향 유통)"
        },
        "phi7_axes": PHI7_LABELS,
        "tools": {
            "phi7_profile": "정치인 7축 프로필 (데이터 기반 자동 계산)",
            "phi7_cross": "두 정치인 Φ7 비교 매트릭스 (보좌관 B2B 핵심)",
            "phi7_policy": "정책 텍스트의 Φ7 축별 영향 예측",
            "phi7_strategy": "Φ7 기반 전략 리포트 (최종 산출물)"
        },
        "target_user": "의원실 보좌진 — 상대 의원 분석·자체 의원 전략 수립",
        "doc_references": [
            "~/dtslib-branch/mcp/README.md",
            "~/dtslib-branch/비즈니스-소설/chan-dae-counter.md (Claude 검증)",
            "~/OrbitPrompt/football-model/mcp/ (원본 Φ드라이버 MCP)"
        ]
    }

# ─── MCP stdio ──────────────────────────────────────────
WELCOME = f"""
╔══════════════════════════════════════════════╗
║  {MCP_NAME} v{VERSION}                       ║
║  Φ-I-C-K-P-7AXIS 정치 분석 (보좌관 B2B)     ║
║  "Φ7 7축이 전부다 — 나머지는 없다"         ║
╚══════════════════════════════════════════════╝

툴 (전부 Φ7 데이터 기반):
  phi7_profile  — 정치인 7축 프로필
  phi7_cross    — 두 정치인 Φ7 비교
  phi7_policy   — 정책 Φ7 영향 예측
  phi7_strategy — Φ7 전략 리포트
  orchestrate   — ★ 메타: 방법론 전체

사용법:
  echo '{{"tool":"phi7_profile","params":{{"politician":"park_chan_dae"}}}}' | python3 server.py
"""

async def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(WELCOME)
        return
    
    request = json.loads(raw)
    tool = request.get("tool", "")
    params = request.get("params", {})
    
    if tool == "phi7_profile":
        r = phi7_profile(params.get("politician", "park_chan_dae"))
        r["_meta"] = {"version": VERSION, "timestamp": datetime.now().isoformat()}
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "phi7_cross":
        r = phi7_cross(
            params.get("politician_a", "park_chan_dae"),
            params.get("politician_b", "park_chan_dae")
        )
        r["_meta"] = {"version": VERSION, "timestamp": datetime.now().isoformat()}
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "phi7_policy":
        r = phi7_policy_impact(
            params.get("politician", "park_chan_dae"),
            params.get("policy_text", "")
        )
        r["_meta"] = {"version": VERSION, "timestamp": datetime.now().isoformat()}
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "phi7_strategy":
        r = phi7_strategy(
            params.get("politician", "park_chan_dae"),
            params.get("agenda", "현안")
        )
        r["_meta"] = {"version": VERSION, "timestamp": datetime.now().isoformat()}
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "orchestrate":
        r = make_orchestrate()
        r["_meta"] = {"version": VERSION, "timestamp": datetime.now().isoformat()}
        print(json.dumps(r, ensure_ascii=False))
    
    else:
        print(json.dumps({
            "_meta": {"version": VERSION, "name": MCP_NAME},
            "welcome": True,
            "tools": [
                {"name": "phi7_profile", "params": {"politician": "park_chan_dae"}},
                {"name": "phi7_cross", "params": {"politician_a": "park_chan_dae", "politician_b": "park_chan_dae"}},
                {"name": "phi7_policy", "params": {"politician": "park_chan_dae", "policy_text": "..."}},
                {"name": "phi7_strategy", "params": {"politician": "park_chan_dae", "agenda": "AI 리터러시"}},
                {"name": "orchestrate", "params": {}},
            ],
            "philosophy": "Φ7 7축 = 전부. 일반 LLM 래퍼 없음. 데이터 기반만."
        }, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
