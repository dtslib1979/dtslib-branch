#!/usr/bin/env python3
"""
server.py — Φ-I-C-K-P-7AXIS 정치 MCP Server (stdio protocol)

박찬대 업무 환경 복제 MCP — 6개 실무 툴 + 1개 메타 툴

사용법:
  echo '{"tool":"policy_brief","params":{"politician":"park_chan_dae","topic":"AI 리터러시"}}' | python3 server.py

툴 목록:
  1. policy_brief     — 정책 브리핑 (Φ드라이버 전략 포함)
  2. policy_analyze   — Φ드라이버 7축 정책 분석
  3. message_draft    — 대외 발언/논평 초안
  4. decision_check   — 안건 검토 + 리스크 분석
  5. local_agenda     — 지역구 의제 트래킹
  6. press_release    — 보도자료/논평 자동 작성
  7. orchestrate      — ★ 메타: 일인 오케스트레이션 방법론 (이 MCP 자체의 설계 철학)

설계 철학:
  이 MCP는 단순한 도구 모음이 아니다.
  Φ-I-C-K-P-7AXIS 철학 모델(OrbitPrompt)이
  특정 정치인(박찬대)의 업무 환경 복제(dtslib-branch)를 통해
  현실 실험(인천·인하대·AI 리터러시)으로 연결되는
  「사고방식 → 도구화 → 배포」 루프의 구현체다.
"""

import sys, json, os, asyncio, textwrap
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from phi7_political import build_politician_profile, analyze_policy_phi7, compare_two_politicians
from model import calc_phi_12, simulate_policy_impact, generate_brief

# ─── 헬퍼 ─────────────────────────────────────────────────
VERSION = "0.1.0"
MCP_NAME = "parksy_political_mcp"

def make_policy_brief(politician_id: str, topic: str) -> dict:
    """툴 1: 정책 브리핑"""
    brief = generate_brief(politician_id, topic)
    profile = calc_phi_12(politician_id)
    return {
        "tool": "policy_brief",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "politician": profile["politician"],
        "topic": topic,
        "brief": brief,
        "phi12_score": profile["phi12_integrated"],
        "usage": "이 브리핑을 회의·메모·보고서 초안으로 활용 가능"
    }

def make_policy_analyze(politician_id: str, policy_text: str) -> dict:
    """툴 2: Φ드라이버 7축 정책 분석"""
    analysis = analyze_policy_phi7(policy_text, politician_id)
    profile = calc_phi_12(politician_id)
    
    # 가상 시뮬레이션
    sim = simulate_policy_impact(politician_id, policy_text)
    
    return {
        "tool": "policy_analyze",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "politician": profile["politician"],
        "phi7_analysis": analysis,
        "phi12_profile": profile,
        "impact_simulation": sim,
        "recommendation": sim["recommendation"]
    }

def make_message_draft(politician_id: str, topic: str, tone: str = "neutral") -> dict:
    """툴 3: 대외 발언/논평 초안"""
    profile = calc_phi_12(politician_id)
    p = build_politician_profile(politician_id)
    
    # Φ드라이버 기반 톤 조정
    tone_map = {
        "aggressive": {"prefix": "강력히 촉구한다", "suffix": "결코 용납할 수 없다"},
        "neutral": {"prefix": "검토가 필요하다", "suffix": "면밀히 살펴보겠다"},
        "positive": {"prefix": "적극 환영한다", "suffix": "함께 만들어가겠다"},
        "cautious": {"prefix": "원칙적으로 동의하나", "suffix": "신중한 접근이 필요하다"},
    }
    t = tone_map.get(tone, tone_map["neutral"])
    
    draft = (
        f"[보도자료/논평 초안 — {datetime.now().strftime('%Y.%m.%d')}]\n\n"
        f"더불어민주당 {p['position']} {p['politician']} 의원은 "
        f"「{topic}」과 관련하여 다음과 같은 입장을 밝혔다.\n\n"
        f"\"{p['politician']} 의원은 {topic}에 대해 {t['prefix']}."
        f" 특히 {p['district']} 지역구와 인천광역시의 관점에서 "
        f"이 문제는 {p['keywords'][0] if p['keywords'] else '시민 삶'}과 "
        f"직결된 사안이다. "
        f"우리 당은 {topic}과 관련된 정책적 대안을 준비 중이며, "
        f"조속한 논의를 위해 관계 기관과 협의해 나갈 것이다. "
        f"이 과정에서 시민 여러분의 의견을 최우선으로 반영하겠다.\"\n\n"
        f"※ {p['politician']} 의원은 {p['education']} 출신으로, "
        f"AI·물류·돌봄 등 인천 미래 비전에 주력하고 있다.\n\n"
        f"[Φ드라이버 톤 분석] Meta:{p['phi7_scores']['meta']} | "
        f"Language:{p['phi7_scores']['language']} | "
        f"Zoom:{p['phi7_scores']['zoom']}"
    )
    
    return {
        "tool": "message_draft",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "politician": p["politician"],
        "topic": topic,
        "tone": tone,
        "draft": draft,
        "char_count": len(draft),
        "estimated_reading_time_sec": len(draft) // 4,
        "phi7_tone_profile": {ax: p["phi7_scores"].get(ax) for ax in ["meta", "language", "zoom"]}
    }

def make_decision_check(politician_id: str, agenda: str, details: str) -> dict:
    """툴 4: 안건 검토 + 리스크 분석"""
    profile = calc_phi_12(politician_id)
    p = build_politician_profile(politician_id)
    
    # 리스크 분석 (키워드 기반 데모)
    risk_keywords = ["예산", "반대", "갈등", "법안", "선거", "스캔들", "논란"]
    found_risks = [kw for kw in risk_keywords if kw in details]
    
    upsides = ["지지율", "공약", "지역", "일자리", "복지", "교육", "AI", "미래"]
    found_upsides = [kw for kw in upsides if kw in details]
    
    risk_score = min(100, len(found_risks) * 20 + (profile["phi7_profile"].get("reverse", 50) < 50) * 30)
    upside_score = min(100, len(found_upsides) * 15 + (profile["phi7_profile"].get("modular", 50) > 60) * 20)
    
    return {
        "tool": "decision_check",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "politician": p["politician"],
        "agenda": agenda,
        "phi12_assessment": {
            "phi12_score": profile["phi12_integrated"],
            "risk_score": risk_score,
            "upside_score": upside_score,
        },
        "risk_factors": [{"keyword": kw, "level": "high" if kw in ["스캔들", "논란", "갈등"] else "medium"} for kw in found_risks],
        "upside_factors": [{"keyword": kw, "level": "high" if kw in ["AI", "미래", "일자리"] else "medium"} for kw in found_upsides],
        "verdict": (
            "추진" if upside_score > risk_score + 20
            else "조건부 추진 — 리스크 보완 후" if upside_score > risk_score
            else "재검토 — 현재 안건은 리스크가 큼"
        ),
        "suggested_actions": [
            f"Φ-{ax}_보강" for ax in ["reverse", "quantum"] 
            if profile["phi7_profile"].get(ax, 50) < 55
        ] + ["보좌진 회의 소집", "관련 위원회 사전 협의"]
    }

def make_local_agenda(politician_id: str, region_focus: str = "") -> dict:
    """툴 5: 지역구 의제 트래킹"""
    p = build_politician_profile(politician_id)
    
    # 기본 지역 의제 템플릿
    agendas = {
        "인천": [
            "인천 경제자유구역 청라·송도·영종 현안",
            "인천 지하철 1호선 연장·검단선",
            "인천공항·인천항 물류 허브 경쟁력",
            "인천형 AI 리터러시 사업 (디지털 배움터 연계)",
            "원도심 재생·주거환경 개선"
        ],
        "default": [
            f"{p['district']} 지역 주요 현안 점검",
            "지역 경제·일자리 동향 모니터링",
            "지역 교육·복지 인프라 현황",
            "지역 주민 대상 정책 수요 조사",
            "지역 언론·여론 동향"
        ]
    }
    
    local = agendas.get(region_focus if region_focus else p["district"], agendas["default"])
    
    # Φ드라이버 기반 우선순위 정렬
    phi7 = p["phi7_scores"]
    priorities = []
    for i, item in enumerate(local):
        priority = min(100, 50 + (i < 2) * 20 + (phi7.get("zoom", 50) > 60) * 15 - i * 5)
        priorities.append({
            "agenda": item,
            "priority": max(10, priority),
            "phi7_relevance": {
                "zoom": min(100, phi7.get("zoom", 50) + (i < 2) * 10),
                "spiral": min(100, phi7.get("spiral", 50) + (i % 3) * 5),
            }
        })
    
    return {
        "tool": "local_agenda",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "politician": p["politician"],
        "district": p["district"],
        "region_focus": region_focus or p["district"],
        "agendas": sorted(priorities, key=lambda x: -x["priority"]),
        "total_items": len(priorities),
        "note": "Φ드라이버 Zoom(중앙↔지역 스케일링) 점수가 높을수록 지역 의제의 국정 연결성이 높음"
    }

def make_press_release(politician_id: str, topic: str, key_message: str) -> dict:
    """툴 6: 보도자료/논평 자동 작성"""
    p = build_politician_profile(politician_id)
    profile = calc_phi_12(politician_id)
    
    # Φ드라이버 기반 보도자료 구조
    name = p["politician"]
    district = p["district"]
    position = p["position"]
    press = (
        f"[보도자료]\n"
        f"제목: {name} 의원, 「{topic}」 관련 입장 발표\n"
        f"일시: {datetime.now().strftime('%Y년 %m월 %d일')}\n"
        f"장소: 국회 소통관 / {district} 지역구 사무실\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"1. {position} {name} 의원은 오늘 "
        f"「{topic}」과 관련한 입장문을 발표하고 "
        f"\"{key_message[:200]}\"라고 밝혔다.\n\n"
        f"2. 특히 {district} 지역 주민들의 생활과 직결된 사안인 만큼, "
        f"{'AI' if 'AI' in topic else '지역'} 관점에서 "
        f"실질적인 대책 마련이 시급하다는 입장이다.\n\n"
        f"3. {name} 의원은 \"{p['key_policies'][0] if p['key_policies'] else '지역 발전'}이라는 "
        f"비전 아래, 이번 {topic}과 관련하여 "
        f"관계 부처와 긴밀히 협의해 나가겠다\"고 덧붙였다.\n\n"
        f"※ 문의: {name} 의원실\n"
        f"※ Φ드라이버 분석: Meta(발언일관성) {p['phi7_scores']['meta']}/100 | "
        f"Lang(프레이밍) {p['phi7_scores']['language']}/100 | "
        f"Zoom(스케일링) {p['phi7_scores']['zoom']}/100\n"
    )
    
    return {
        "tool": "press_release",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "politician": p["politician"],
        "topic": topic,
        "press_release": press,
        "char_count": len(press),
        "estimated_reading_time_sec": len(press) // 3,
        "phi12_profile": profile,
        "distribution_suggestions": [
            f"국회 소통관 배포",
            f"{p['district']} 지역 언론 ({len(p['keywords'])}+매체)",
            f"당내 정책위원회 공유",
            f"SNS (메시지 발췌본 3개 제안: 핵심/감성/데이터)"
        ]
    }

def make_orchestrate() -> dict:
    """
    ★ 툴 7: 메타 — 일인 오케스트레이션 방법론
    
    이 MCP 자체의 설계 철학과 작동 방식을 반환한다.
    하나의 시민(박씨)이 Perplexity/DeepSeek/Claude/레포를
    오케스트레이션해서 정치인의 업무 환경을 복제하는 방법론.
    
    이 툴이 이 MCP를 메타 MCP로 만든다.
    """
    return {
        "tool": "orchestrate",
        "version": VERSION,
        "name": "일인 오케스트레이션 에이전트 협업 방법론",
        "description": (
            "시민 1인이 AI 에이전트(Perplexity/DeepSeek/Claude)를 "
            "오케스트레이션해서 정치인의 업무 환경을 복제하고, "
            "정책·커뮤니케이션 모듈을 생산한 뒤, "
            "GitHub MCP 배포를 통해 정치인→시민 역방향 유통을 실현하는 "
            "AI 시대 민주주의 참여 방법론"
        ),
        "architecture": {
            "layers": {
                "orbitprompt": {
                    "role": "사고 실험실 — Φ드라이버·7축·철학 모델",
                    "owner": "박씨 (아이디어)",
                    "tools": ["개념어 사전", "Φ-I-C-K-P-7AXIS", "ENDPOINT 모델"]
                },
                "dtslib_branch": {
                    "role": "현실 접속 레포 — 비즈니스 소설·사례·정치 MCP",
                    "owner": "DeepSeek (구현) + Claude (검증)",
                    "tools": ["정치 MCP server.py", "백서 HTML", "워크로그"]
                },
                "현실_실험": {
                    "role": "실제 정치인·도시·교육 현장",
                    "owner": "박찬대·인하대·인천시 (파트너)",
                    "tools": ["PPT", "커리큘럼", "제안서"]
                }
            },
            "agents": {
                "박씨": {"role": "정치인 = 최종 판단자", "domain": "방향 설정·결재"},
                "Perplexity": {"role": "정책 브리핑·회의 파트너", "domain": "구조화·논리·서사"},
                "DeepSeek": {"role": "구현 보좌관", "domain": "MCP 코딩·초안 생산"},
                "Claude": {"role": "비서실장·검증", "domain": "카운터·레포 정합성"}
            },
            "delivery": {
                "primary": "GitHub 공개 레포 (MCP server.py = 자가실행)",
                "secondary": "SD카드 로컬 서버 (E:/mcp/)",
                "tertiary": "Railway 백업 (YouTube 반응 기반)"
            }
        },
        "flow": (
            "OrbitPrompt(철학) → Φ드라이버 MCP(도구화) → "
            "dtslib-branch(사례·백서) → 현실 실험(인천/인하대)"
        ),
        "key_insight": (
            "이 방법론이 '그냥 시민 의견'과 다른 점은: "
            "1) 생산된 모듈이 LLM+레포로 지속 가능하고 "
            "2) MCP 구조로 타인도 재사용 가능하며 "
            "3) GitHub 역방향 유통으로 정치인→시민 동선이 아닌 "
            "시민→정치인 동선을 만든다는 것"
        ),
        "politician_simulation_models": [
            {
                "type": "아바타 접신",
                "description": "정치인 업무 환경 복제 → 그 안에서 판단 시뮬레이션"
            },
            {
                "type": "정책 SCM",
                "description": "시민+AI가 설계한 정책 모듈을 정치인이 꽂는 공급망"
            },
            {
                "type": "역방향 유통",
                "description": "GitHub MCP → 정치인이 찾아오는 구조 (전통 로비 동선의 역전)"
            }
        ],
        "doc_references": [
            "~/OrbitPrompt/boards/chan-dae-project.md (연결맵)",
            "~/dtslib-branch/비즈니스-소설/chan-dae-worklog.md (작업 로그)",
            "~/dtslib-branch/비즈니스-소설/chan-dae-counter.md (Claude 검증)",
            "~/dtslib-branch/비즈니스-소설/박찬대-되기-프로젝트.html (백서)",
            "~/OrbitPrompt/football-model/mcp/ (원본 Φ드라이버 MCP)"
        ]
    }

# ─── MCP stdio protocol ─────────────────────────────
WELCOME = f"""
╔══════════════════════════════════════════════╗
║  {MCP_NAME} v{VERSION}                       ║
║  Φ-I-C-K-P-7AXIS 정치 분석 MCP              ║
║  "사고방식이 도구가 되는 순간"              ║
╚══════════════════════════════════════════════╝

툴 목록:
  policy_brief    — 정책 브리핑 (Φ드라이버 전략)
  policy_analyze  — Φ7축 정책 분석 + 영향 시뮬레이션
  message_draft   — 대외 발언/논평 초안
  decision_check  — 안건 검토 + 리스크 분석
  local_agenda    — 지역구 의제 트래킹
  press_release   — 보도자료 자동 작성
  orchestrate     — ★ 메타: 방법론 전체 구조

사용법:
  echo '{{"tool":"<tool>","params":{{...}}}}' | python3 server.py
"""

async def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(WELCOME)
        return
    
    request = json.loads(raw)
    tool = request.get("tool", "")
    params = request.get("params", {})
    
    if tool == "policy_brief":
        r = make_policy_brief(
            params.get("politician", "park_chan_dae"),
            params.get("topic", "AI 리터러시")
        )
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "policy_analyze":
        r = make_policy_analyze(
            params.get("politician", "park_chan_dae"),
            params.get("policy_text", "")
        )
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "message_draft":
        r = make_message_draft(
            params.get("politician", "park_chan_dae"),
            params.get("topic", "현안"),
            params.get("tone", "neutral")
        )
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "decision_check":
        r = make_decision_check(
            params.get("politician", "park_chan_dae"),
            params.get("agenda", ""),
            params.get("details", "")
        )
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "local_agenda":
        r = make_local_agenda(
            params.get("politician", "park_chan_dae"),
            params.get("region_focus", "")
        )
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "press_release":
        r = make_press_release(
            params.get("politician", "park_chan_dae"),
            params.get("topic", ""),
            params.get("key_message", "")
        )
        print(json.dumps(r, ensure_ascii=False))
    
    elif tool == "orchestrate":
        r = make_orchestrate()
        print(json.dumps(r, ensure_ascii=False))
    
    else:
        print(json.dumps({
            "welcome": True,
            "name": MCP_NAME,
            "version": VERSION,
            "tools": [
                {"name": "policy_brief", "params": {"politician": "park_chan_dae", "topic": "AI 리터러시"}},
                {"name": "policy_analyze", "params": {"politician": "park_chan_dae", "policy_text": "..."}},
                {"name": "message_draft", "params": {"politician": "park_chan_dae", "topic": "...", "tone": "neutral"}},
                {"name": "decision_check", "params": {"politician": "park_chan_dae", "agenda": "...", "details": "..."}},
                {"name": "local_agenda", "params": {"politician": "park_chan_dae", "region_focus": "인천"}},
                {"name": "press_release", "params": {"politician": "park_chan_dae", "topic": "...", "key_message": "..."}},
                {"name": "orchestrate", "params": {}},
            ],
            "philosophy": "Φ-I-C-K-P-7AXIS — OrbitPrompt 철학의 정치 포팅",
            "doc": "~/dtslib-branch/mcp/README.md"
        }, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
