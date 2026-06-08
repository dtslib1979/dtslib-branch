#!/usr/bin/env python3
"""
model.py — Φ-I-C-K-P-7AXIS 정치 분석 모델

축구 MCP(OrbitPrompt/football-model/mcp/model.py)의 정치 포팅.
동일한 12차원 구조: 5변수(Φ-I-C-K-P) + 7드라이버(정치인/정책 데이터)

레이어:
  Φ5  = 기본 정치인 프로필 (소속·지역·경력)
  Φ7  = 7드라이버 동적 점수 (발언·행적·정책)
  Φ12 = 통합 정치 분석 점수
"""

import sys, json, os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from phi7_political import build_politician_profile, analyze_policy_phi7, compare_two_politicians, POLITICIANS

# ─── Φ5: 기본 프로필 점수 ────────────────────────────────
def calc_phi5(politician_id: str) -> float:
    """기본 프로필 기반 점수 (경력·소속·교육·키워드)"""
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    
    score = 50  # 기본값
    
    # 경력 보유
    if info["position"] != "보직":
        score += 10
    
    # 교육
    if info["education"] != "학력":
        score += 5
    
    # 키워드 다양성
    score += min(20, len(info["keywords"]) * 3)
    
    # 정책 다양성
    score += min(15, len(info["key_policies"]) * 3)
    
    return min(100, max(0, score))

# ─── Φ7 → Φ12 통합 ──────────────────────────────────────
AXIS_WEIGHTS = {
    "meta": 1.2,      # 발언 일관성 (신뢰도 핵심)
    "reverse": 1.3,   # 위기 대응력 (정치 생존)
    "modular": 1.0,   # 정책 조합력
    "language": 1.1,  # 프레이밍 (커뮤니케이션)
    "zoom": 1.2,      # 스케일링 (중앙↔지역)
    "spiral": 1.0,    # 모멘텀
    "quantum": 0.8,   # 변수 중첩 (혁신성)
}
PHI7_WEIGHT = 0.35  # Φ12에서 Φ7 비중

def calc_phi7_score(politician_id: str) -> float:
    """7드라이버 통합 점수"""
    p = build_politician_profile(politician_id)
    scores = p["phi7_scores"]
    raw = sum(scores.get(ax, 50) * AXIS_WEIGHTS.get(ax, 1.0) for ax in AXIS_WEIGHTS)
    return round(raw / (100 * sum(AXIS_WEIGHTS.values())) * 100, 1)

def calc_phi_12(politician_id: str) -> dict:
    """Φ12 통합 점수 = Φ5 × (1-PHI7_WEIGHT) + Φ7 × PHI7_WEIGHT"""
    s5 = calc_phi5(politician_id)
    s7 = calc_phi7_score(politician_id)
    c = round(s5 * (1 - PHI7_WEIGHT) + s7 * PHI7_WEIGHT, 1)
    p = build_politician_profile(politician_id)
    return {
        "politician": p["politician"],
        "id": politician_id,
        "phi5_profile": s5,
        "phi7_dynamic": s7,
        "phi12_integrated": c,
        "phi7_profile": p["phi7_scores"],
        "phi7_descriptions": p["phi7_descriptions"]
    }

# ─── 정책 시뮬레이션 ──────────────────────────────────────
def simulate_policy_impact(politician_id: str, policy_text: str) -> dict:
    """
    정책이 정치인 7축에 미치는 영향 시뮬레이션
    = 가상의 정책을 도입했을 때 각 축 점수 변화 예측
    """
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    current = build_politician_profile(politician_id)
    policy_analysis = analyze_policy_phi7(policy_text, politician_id)
    
    # 정책 도입 후 예상 변화 (데모)
    delta = {}
    for ax in AXIS_WEIGHTS:
        original = current["phi7_scores"].get(ax, 50)
        boost = (policy_analysis["phi7_scores"].get(ax, 50) - 50) * 0.3
        delta[ax] = {
            "before": original,
            "after": round(min(100, max(0, original + boost)), 1),
            "change": round(boost, 1)
        }
    
    avg_before = round(sum(current["phi7_scores"].get(ax, 50) for ax in AXIS_WEIGHTS) / 7, 1)
    avg_after = round(sum(delta[ax]["after"] for ax in AXIS_WEIGHTS) / 7, 1)
    
    return {
        "politician": info["name"],
        "policy_summary": policy_text[:100] + ("..." if len(policy_text) > 100 else ""),
        "phi7_change": delta,
        "average_before": avg_before,
        "average_after": avg_after,
        "net_impact": round(avg_after - avg_before, 1),
        "recommendation": (
            "적극 추천 — 정책 도입 시 종합 점수 상승"
            if avg_after > avg_before + 3
            else "검토 필요 — 영향이 제한적"
            if avg_after >= avg_before - 2
            else "비권장 — 정책이 정치인 프로필에 부정적"
        )
    }

# ─── 시나리오 브리핑 생성 ────────────────────────────────
def generate_brief(politician_id: str, topic: str) -> str:
    """특정 의제에 대한 정치인 맞춤 브리핑 (Φ드라이버 기반)"""
    profile = calc_phi_12(politician_id)
    p = profile["phi7_profile"]
    
    brief = []
    brief.append(f"📋 Φ-I-C-K-P-7AXIS 정책 브리핑")
    brief.append(f"━━━━━━━━━━━━━━━━━━━━━━")
    brief.append(f"대상: {profile['politician']} | 의제: {topic}")
    brief.append(f"Φ12 통합 점수: {profile['phi12_integrated']}/100")
    brief.append("")
    
    axis_advice = {
        "meta": f"  【발언 일관성 {p['meta']}/100】 — '{topic}' 관련 과거 입장과의 정합성 점검 필요",
        "reverse": f"  【위기 대응 {p['reverse']}/100】 — '{topic}' 반대 여론·역풍 시나리오 대비",
        "modular": f"  【정책 조합 {p['modular']}/100】 — '{topic}'와 기존 공약 패키지와의 연결성",
        "language": f"  【프레이밍 {p['language']}/100】 — '{topic}' 메시지 구조·수사 전략 설계",
        "zoom": f"  【스케일링 {p['zoom']}/100】 — '{topic}'의 중앙 정책과 지역구 연결 지점",
        "spiral": f"  【모멘텀 {p['spiral']}/100】 — '{topic}' 발의 최적 타이밍·사이클 분석",
        "quantum": f"  【변수 중첩 {p['quantum']}/100】 — '{topic}' 관련 예측불가 변수 리스트업",
    }
    
    brief.append("【Φ드라이버별 전략】")
    for ax_name in ["meta", "reverse", "modular", "language", "zoom", "spiral", "quantum"]:
        brief.append(axis_advice[ax_name])
    
    brief.append("")
    brief.append(f"【종합】 {profile['politician']}에게 '{topic}'는")
    avg_p = sum(p.values()) / 7
    if avg_p >= 70:
        brief.append(f"  적극 추진 가능한 의제 — Φ12 {profile['phi12_integrated']}/100, 현재 프로필과 정합")
    elif avg_p >= 50:
        brief.append(f"  조건부 추진 — 일부 축(취약점) 보완 후 발의 권장")
    else:
        brief.append(f"  현재 프로필과 거리 있음 — 의제 재정의 또는 추진 시기 재검토")
    
    return "\n".join(brief)

if __name__ == "__main__":
    if "--phi12" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--phi12")
        print(json.dumps(calc_phi_12(sys.argv[i+1]), indent=2, ensure_ascii=False))
    elif "--simulate" in sys.argv and len(sys.argv) >= 4:
        i = sys.argv.index("--simulate")
        print(json.dumps(simulate_policy_impact(sys.argv[i+1], sys.argv[i+2]), indent=2, ensure_ascii=False))
    elif "--brief" in sys.argv and len(sys.argv) >= 4:
        i = sys.argv.index("--brief")
        print(generate_brief(sys.argv[i+1], sys.argv[i+2]))
    elif "--list" in sys.argv:
        for pid in POLITICIANS:
            r = calc_phi_12(pid)
            print(f"{r['politician']:20s} Φ5:{r['phi5_profile']:>5.1f} Φ7:{r['phi7_dynamic']:>5.1f} Φ12:{r['phi12_integrated']:>5.1f}")
    else:
        print("--phi12 <politician> | --simulate <politician> <policy_text> | --brief <politician> <topic> | --list")
