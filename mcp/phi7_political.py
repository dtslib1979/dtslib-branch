#!/usr/bin/env python3
"""
phi7_political.py — 7드라이버 정치 버전 (v2: 보좌관 B2B 타겟)

형(Claude) 카운터 #003 반영:
  - Φ드라이버가 전부여야 함. 일반 LLM 래퍼 금지
  - 타겟: 일반 시민 ❌ → 다른 의원실 보좌관 ✅

Φ드라이버 매핑:
  Meta     → 발언 일관성 (과거 vs 현재 입장 안정성)
  Reverse  → 위기 대응력 (역전/스캔들 시나리오)
  Modular  → 정책 조합력 (공약 패키지 설계 능력)
  Language → 프레이밍/수사 전략 (메시지 구조)
  Zoom     → 중앙↔지역 스케일링 (국정↔지역구)
  Spiral   → 정치 사이클 (모멘텀 곡선/이슈 증폭)
  Quantum  → 변수 중첩 (예측불가·다중 이해관계)
"""

import sys, json, math
from datetime import datetime

# ─── 정치인 DB ─────────────────────────────────────────
POLITICIANS = {
    "park_chan_dae": {
        "name": "박찬대",
        "party": "더불어민주당",
        "district": "인천 연수구",
        "position": "국회의원·원내대표",
        "education": "인하대 경영학과",
        "career_years": 8,
        "committee": ["정무위원회", "AI특별위원회"],
        "keywords": ["AI", "인천", "물류", "돌봄", "경영", "회계사"],
        "key_policies": ["AI 도시 인천", "노인 AI 리터러시", "인천 물류 허브"],
        "speeches": 120,
        "bills": 18,
        "media_interviews": 45
    },
    "opposition_sample": {
        "name": "홍길동",
        "party": "국민의힘",
        "district": "서울 강남구",
        "position": "국회의원·정책위원회 간사",
        "education": "서울대 법학과",
        "career_years": 12,
        "committee": ["법제사법위원회", "예산결산특별위원회"],
        "keywords": ["법률", "예산", "보수", "규제개혁", "강남"],
        "key_policies": ["규제 혁파", "법치주의 강화", "재정 건전성"],
        "speeches": 200,
        "bills": 35,
        "media_interviews": 80
    },

    "default": {
        "name": "정치인",
        "party": "정당",
        "district": "지역구",
        "position": "보직",
        "education": "",
        "career_years": 0,
        "committee": [],
        "keywords": [],
        "key_policies": [],
        "speeches": 0,
        "bills": 0,
        "media_interviews": 0
    }
}

# ─── 7축 계산 (데이터 기반) ───────────────────────────
PHI7_LABELS = {
    "meta": "발언 일관성 — 과거 입장과 현재의 정합성",
    "reverse": "위기 대응 — 스캔들·역풍·반대파 대응력",
    "modular": "정책 조합 — 공약·법안·사업의 패키지 설계력",
    "language": "프레이밍 — 메시지 구조화·수사·내러티브",
    "zoom": "스케일링 — 중앙정치↔지역구 연결 능력",
    "spiral": "모멘텀 — 이슈 증폭·타이밍·사이클 이해",
    "quantum": "변수 중첩 — 예측불가·다중이해관계 해석"
}

def calc_phi7_scores(politician_id: str) -> dict:
    """
    정치인 데이터로 7축 점수 자동 계산
    보좌관이 보는 데이터 기반 분석 리포트
    """
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    
    # Meta: 발언 일관성 = 발언 수 × 경력 대비 법안 비율
    meta = min(95, 50 + min(info["speeches"], 200) * 0.12 + info["bills"] * 1.5)
    
    # Reverse: 위기 대응 = 경력년수 × 위원회 다양성
    reverse = min(95, 40 + info["career_years"] * 3 + len(info["committee"]) * 8)
    
    # Modular: 정책 조합 = 정책 수 × 키워드 다양성
    modular = min(95, 45 + len(info["key_policies"]) * 8 + len(info["keywords"]) * 4)
    
    # Language: 프레이밍 = 미디어 노출 × 교육 배경
    edu_bonus = 10 if info["education"] else 0
    language = min(95, 40 + min(info["media_interviews"], 100) * 0.4 + edu_bonus)
    
    # Zoom: 스케일링 = 지역구 × 중앙위원회
    zoom = min(95, 50 + len(info["committee"]) * 10 + info["career_years"] * 2)
    
    # Spiral: 모멘텀 = 법안 수 × 발언 수 균형
    spiral = min(95, 45 + info["bills"] * 1.2 + min(info["speeches"], 150) * 0.1)
    
    # Quantum: 변수 중첩 = 키워드 다양성 × 위원회 교차
    quantum = min(95, 40 + len(info["keywords"]) * 5 + len(info["committee"]) * 6)
    
    return {
        "meta": round(meta, 1),
        "reverse": round(reverse, 1),
        "modular": round(modular, 1),
        "language": round(language, 1),
        "zoom": round(zoom, 1),
        "spiral": round(spiral, 1),
        "quantum": round(quantum, 1)
    }

# ─── 핵심 함수 ──────────────────────────────────────────

def phi7_profile(politician_id: str) -> dict:
    """툴 1: 정치인 7축 프로필 (Core)"""
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    scores = calc_phi7_scores(politician_id)
    avg = round(sum(scores.values()) / 7, 1)
    
    # 축별 강/약 판정
    strengths = {k: v for k, v in scores.items() if v >= 70}
    weaknesses = {k: v for k, v in scores.items() if v < 55}
    
    # 종합 전략
    if avg >= 75:
        grade = "S"
        summary = "종합 S급 — 전개 가능한 정치인. 보좌진은 개별 축 보강만."
    elif avg >= 65:
        grade = "A"
        summary = "종합 A급 — 특정 축(Reverse/Quantum) 보강 시 S급 도달 가능"
    elif avg >= 55:
        grade = "B"
        summary = "종합 B급 — 핵심 취약축 2~3개 집중 보강 필요"
    else:
        grade = "C"
        summary = "종합 C급 — 기초 데이터 부족. 프로필 재구축 권장"
    
    return {
        "tool": "phi7_profile",
        "politician": info["name"],
        "party": info["party"],
        "position": info["position"],
        "district": info["district"],
        "phi7_scores": scores,
        "phi7_labels": PHI7_LABELS,
        "phi7_average": avg,
        "grade": grade,
        "summary": summary,
        "strengths": list(strengths.keys()),
        "weaknesses": list(weaknesses.keys()),
        "source_data": {
            "career_years": info["career_years"],
            "bills": info["bills"],
            "speeches": info["speeches"],
            "media_interviews": info["media_interviews"],
            "committees": info["committee"]
        }
    }

def phi7_cross(id_a: str, id_b: str) -> dict:
    """툴 2: 두 정치인 7축 비교 매트릭스 (B2B 핵심)"""
    a_info = POLITICIANS.get(id_a, POLITICIANS["default"])
    b_info = POLITICIANS.get(id_b, POLITICIANS["default"])
    a_scores = calc_phi7_scores(id_a)
    b_scores = calc_phi7_scores(id_b)
    
    axes = list(PHI7_LABELS.keys())
    comparison = {}
    total_diff = 0
    advantages_a = 0
    advantages_b = 0
    
    for ax in axes:
        sa = a_scores[ax]
        sb = b_scores[ax]
        diff = round(sa - sb, 1)
        total_diff += diff
        if diff > 3: advantages_a += 1
        elif diff < -3: advantages_b += 1
        comparison[ax] = {
            "a_score": sa, "b_score": sb,
            "diff": diff,
            "advantage": id_a if diff > 3 else id_b if diff < -3 else "even",
            "description": (
                f"{a_info['name']}({sa}) vs {b_info['name']}({sb}) — "
                f"{'우세' if diff > 3 else '열세' if diff < -3 else '대등'}"
            )
        }
    
    a_avg = round(sum(a_scores.values()) / 7, 1)
    b_avg = round(sum(b_scores.values()) / 7, 1)
    
    # 전력 분석 리포트
    report = []
    report.append(f"【Φ7 비교: {a_info['name']} vs {b_info['name']}】")
    report.append(f"  종합 {a_info['name']}: {a_avg} / {b_info['name']}: {b_avg}")
    report.append(f"  {a_info['name']} 우세: {advantages_a}개 축")
    report.append(f"  {b_info['name']} 우세: {advantages_b}개 축")
    report.append("")
    
    # 결정적 차이가 있는 축
    decisive = sorted(comparison.items(), key=lambda x: abs(x[1]["diff"]), reverse=True)
    report.append("【결정적 차이 축】")
    for ax, data in decisive[:3]:
        if abs(data["diff"]) > 5:
            report.append(f"  {ax}: 차이 {data['diff']} — {PHI7_LABELS[ax].split(' — ')[0]}")
    
    winner = id_a if total_diff > 10 else id_b if total_diff < -10 else "even"
    margin = round(abs(total_diff), 1)
    
    return {
        "tool": "phi7_cross",
        "politician_a": {"id": id_a, "name": a_info["name"], "party": a_info["party"], "avg": a_avg},
        "politician_b": {"id": id_b, "name": b_info["name"], "party": b_info["party"], "avg": b_avg},
        "axis_comparison": comparison,
        "advantages": {id_a: advantages_a, id_b: advantages_b},
        "verdict": (
            f"{a_info['name']} 우세 ({margin}점 차)"
            if winner == id_a
            else f"{b_info['name']} 우세 ({margin}점 차)"
            if winner == id_b
            else "대등 (5점 이내 차이)"
        ),
        "report": "\n".join(report),
        "b2b_usage": "보좌관이 상대 의원 7축 분석·대응 전략 수립용"
    }

def phi7_policy_impact(politician_id: str, policy_text: str) -> dict:
    """툴 3: 정책의 7축 영향 예측"""
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    base = calc_phi7_scores(politician_id)
    
    # 정책 텍스트 분석 → 축별 가중치 (데모: 텍스트 길이/키워드 기반)
    word_count = len(policy_text.split())
    has_local = "지역" in policy_text or "인천" in policy_text
    has_ai = "AI" in policy_text or "인공지능" in policy_text
    has_future = "미래" in policy_text or "전환" in policy_text or "혁신" in policy_text
    has_welfare = "복지" in policy_text or "돌봄" in policy_text or "약자" in policy_text
    has_biz = "기업" in policy_text or "경제" in policy_text or "일자리" in policy_text
    
    # 축별 영향 계산
    deltas = {}
    deltas["meta"] = round(2 if has_ai else -1 if not has_local else 0, 1)
    deltas["reverse"] = round(-3 if "예산" in policy_text else 1, 1)
    deltas["modular"] = round(3 if has_ai and has_welfare else 1, 1)
    deltas["language"] = round(2 if has_future else 1, 1)
    deltas["zoom"] = round(4 if has_local else 0, 1)
    deltas["spiral"] = round(3 if has_future else 1, 1)
    deltas["quantum"] = round(-2 if "예산" in policy_text else 2 if has_biz else 0, 1)
    
    after = {}
    for ax in base:
        after[ax] = round(min(100, max(0, base[ax] + deltas[ax])), 1)
    
    avg_before = round(sum(base.values()) / 7, 1)
    avg_after = round(sum(after.values()) / 7, 1)
    
    return {
        "tool": "phi7_policy",
        "politician": info["name"],
        "policy_length": word_count,
        "phi7_before": base,
        "phi7_after": after,
        "deltas": deltas,
        "average_before": avg_before,
        "average_after": avg_after,
        "net_impact": round(avg_after - avg_before, 1),
        "policy_features": {
            "local_focus": has_local,
            "ai_related": has_ai,
            "future_oriented": has_future,
            "welfare_included": has_welfare,
            "business_economy": has_biz
        },
        "recommendation": (
            "도입 시 종합 점수 상승 — 정책이 Φ7 프로필과 정합"
            if avg_after > avg_before + 2
            else "영향 제한적 — 정책 재구성 또는 다른 의제 검토"
            if avg_after >= avg_before - 1
            else "비권장 — 정책이 정치인 프로필에 부정적 영향"
        )
    }

def phi7_strategy(politician_id: str, agenda: str) -> dict:
    """툴 4: 7축 기반 전략 리포트 (보좌관 최종 산출물)"""
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    scores = calc_phi7_scores(politician_id)
    avg = round(sum(scores.values()) / 7, 1)
    
    # 취약축 보강 전략
    strategy = []
    strategy.append(f"【Φ7 전략 리포트: {info['name']} — '{agenda}'】")
    strategy.append(f"Φ7 평균: {avg}/100 | 등급: {'S' if avg>=75 else 'A' if avg>=65 else 'B'}")
    strategy.append("")
    
    # 축별 전략
    for ax in PHI7_LABELS:
        score = scores[ax]
        label = PHI7_LABELS[ax].split(" — ")[0]
        if score >= 75:
            level = "✅ 강점"
            action = "현재 수준 유지. 이 축을 활용한 메시지 전략 전개"
        elif score >= 60:
            level = "📊 보통"
            action = f"{agenda}와 연결하여 추가 보강 가능"
        else:
            level = "⚠️ 취약"
            action = f"집중 보강 필요. {agenda} 전에 최소 3회 보강 액션 권장"
        
        strategy.append(f"  {level} {label}({score}): {action}")
    
    strategy.append("")
    
    # 최우선 액션
    weakest = min(scores, key=scores.get)
    strongest = max(scores, key=scores.get)
    strategy.append("【최우선 액션 아이템】")
    strategy.append(f"  1. 취약축 보강: {PHI7_LABELS[weakest].split(' — ')[0]} ({scores[weakest]})")
    strategy.append(f"  2. 강점축 활용: {PHI7_LABELS[strongest].split(' — ')[0]} ({scores[strongest]})을 '{agenda}' 프레임에 연결")
    strategy.append(f"  3. 타이밍: Spiral({scores['spiral']}) 모멘텀 점검 → 발의 시기 결정")
    
    return {
        "tool": "phi7_strategy",
        "politician": info["name"],
        "agenda": agenda,
        "phi7_scores": scores,
        "phi7_average": avg,
        "strategy": "\n".join(strategy),
        "weakest_axis": weakest,
        "strongest_axis": strongest,
        "target_audience": "의원실 보좌진 (정책·메시지·일정 전략 수립용)"
    }

if __name__ == "__main__":
    if "--profile" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--profile")
        print(json.dumps(phi7_profile(sys.argv[i+1]), indent=2, ensure_ascii=False))
    elif "--compare" in sys.argv and len(sys.argv) >= 4:
        i = sys.argv.index("--compare")
        print(json.dumps(phi7_cross(sys.argv[i+1], sys.argv[i+2]), indent=2, ensure_ascii=False))
    elif "--table" in sys.argv:
        print(f"{'Politician':25s} {'Meta':>6s} {'Rev':>6s} {'Mod':>6s} {'Lang':>6s} {'Zoom':>6s} {'Spir':>6s} {'Quan':>6s} {'Avg':>6s}")
        print("-" * 75)
        for pid in POLITICIANS:
            p = phi7_profile(pid)
            s = p["phi7_scores"]
            print(f"{p['politician']:25s} {s['meta']:>5.1f} {s['reverse']:>5.1f} {s['modular']:>5.1f} {s['language']:>5.1f} {s['zoom']:>5.1f} {s['spiral']:>5.1f} {s['quantum']:>5.1f} {p['phi7_average']:>5.1f}")
