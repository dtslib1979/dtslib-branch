#!/usr/bin/env python3
"""
phi7_political.py — 7축 드라이버 정치 버전

Φ드라이버를 정치인·정책 분석용으로 리매핑:
  Meta     → 발언 일관성 (과거 vs 현재 입장 안정성)
  Reverse  → 위기 대응력 (역전/스캔들 시나리오)
  Modular  → 정책 조합력 (공약 패키지 설계 능력)
  Language → 프레이밍/수사 전략 (메시지 구조)
  Zoom     → 중앙↔지역 스케일링 (국정↔지역구)
  Spiral   → 정치 사이클 (모멘텀 곡선/이슈 증폭)
  Quantum  → 변수 중첩 (예측불가·다중 이해관계)

출처: OrbitPrompt Φ-I-C-K-P-7AXIS 철학 모델
       football-model/mcp/phi7_driver.py 의 정치 포팅
"""

import sys, json, os, re
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))

# ─── 정치인 기본 데이터 ───────────────────────────────────
POLITICIANS = {
    "park_chan_dae": {
        "name": "박찬대",
        "party": "더불어민주당",
        "district": "인천 연수구",
        "position": "국회의원 · 원내대표",
        "education": "인하대 경영학과",
        "keywords": ["AI", "인천", "물류", "돌봄", "경영", "회계사"],
        "key_policies": [
            "AI 도시 인천 비전",
            "노인·약자 AI 리터러시",
            "인천 물류 허브",
            "지역 돌봄 인프라"
        ]
    },
    "default": {
        "name": "정치인",
        "party": "정당",
        "district": "지역구",
        "position": "보직",
        "education": "학력",
        "keywords": [],
        "key_policies": []
    }
}

# ─── 7축 점수 (데이터 기반 자동 계산) ────────────────────
# 실제 구현 시: 뉴스·발언·법안·지지율 데이터 수집 → 자동 계산
# 현재: 데모 모드 (수동 입력 + 기본값)

def build_politician_profile(politician_id: str, manual_scores: dict = None) -> dict:
    """
    정치인 7축 프로필 생성
    manual_scores: {"meta": 85, "reverse": 70, ...} 수동 입력 가능
    """
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    
    if manual_scores:
        scores = manual_scores
    else:
        # 데모 기본값 (실제 계산 전까지)
        scores = {
            "meta": 75,      # 발언 일관성
            "reverse": 65,   # 위기 대응력
            "modular": 80,   # 정책 조합력
            "language": 70,  # 프레이밍 전략
            "zoom": 85,      # 중앙↔지역 스케일링
            "spiral": 60,    # 정치 사이클
            "quantum": 55,   # 변수 중첩
        }
    
    return {
        "politician": info["name"],
        "id": politician_id,
        "party": info["party"],
        "district": info["district"],
        "position": info["position"],
        "education": info["education"],
        "keywords": info["keywords"],
        "key_policies": info["key_policies"],
        "phi7_scores": scores,
        "phi7_descriptions": {
            "meta": "발언 일관성 — 과거 입장과 현재 입장의 정합성",
            "reverse": "위기 대응력 — 역전/스캔들 상황의 대처 능력",
            "modular": "정책 조합력 — 공약·정책의 모듈式 설계 능력",
            "language": "프레이밍 — 메시지 구조화·수사 전략",
            "zoom": "스케일링 — 중앙 정치와 지역구 의제 연결 능력",
            "spiral": "모멘텀 — 정치 사이클·이슈 증폭·타이밍",
            "quantum": "변수 중첩 — 다중 이해관계·예측불가 상황 해석"
        }
    }

def analyze_policy_phi7(policy_text: str, politician_id: str = "default") -> dict:
    """
    정책 텍스트를 Φ드라이버 7축으로 분석
    각 축별 점수 + 종합 평가
    """
    info = POLITICIANS.get(politician_id, POLITICIANS["default"])
    
    # 텍스트 길이/키워드 기반 간소 분석 (실제: LLM 호출)
    keywords = set(info["keywords"])
    word_count = len(policy_text.split())
    
    # 정책 분석 점수 (데모)
    scores = {
        "meta": min(100, 50 + word_count // 10),
        "reverse": min(100, 40 + (word_count % 20)),
        "modular": min(100, 60 + sum(1 for k in keywords if k in policy_text) * 10),
        "language": min(100, 55 + (policy_text.count("것입니다") > 0) * 20),
        "zoom": min(100, 50 + (("지역" in policy_text) * 15) + (("국가" in policy_text) * 15)),
        "spiral": min(100, 45 + (("시대" in policy_text or "전환" in policy_text) * 25)),
        "quantum": min(100, 40 + policy_text.count("동시에") * 10 + policy_text.count("그러나") * 10),
    }
    
    avg = sum(scores.values()) / 7
    grade = "S" if avg >= 85 else "A" if avg >= 70 else "B" if avg >= 55 else "C"
    
    return {
        "politician": info["name"],
        "policy_length": word_count,
        "phi7_scores": scores,
        "average": round(avg, 1),
        "grade": grade,
        "assessment": (
            "종합적으로 우수한 정책 설계" if grade == "S"
            else "대체로 균형 잡힌 정책" if grade == "A"
            else "일부 축 보강 필요" if grade == "B"
            else "전면 재검토 권장"
        )
    }

def compare_two_politicians(id_a: str, id_b: str) -> dict:
    """두 정치인 7축 비교"""
    a = build_politician_profile(id_a)
    b = build_politician_profile(id_b)
    
    axes = ["meta", "reverse", "modular", "language", "zoom", "spiral", "quantum"]
    diff = {}
    for ax in axes:
        sa = a["phi7_scores"].get(ax, 50)
        sb = b["phi7_scores"].get(ax, 50)
        diff[ax] = {"a": sa, "b": sb, "diff": round(sa - sb, 1)}
    
    avg_a = sum(a["phi7_scores"].get(ax, 50) for ax in axes) / 7
    avg_b = sum(b["phi7_scores"].get(ax, 50) for ax in axes) / 7
    
    return {
        "politician_a": {"name": a["politician"], "id": id_a, "avg": round(avg_a, 1)},
        "politician_b": {"name": b["politician"], "id": id_b, "avg": round(avg_b, 1)},
        "axis_comparison": diff,
        "winner": id_a if avg_a > avg_b else id_b,
        "margin": round(abs(avg_a - avg_b), 1)
    }

if __name__ == "__main__":
    if "--profile" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--profile")
        print(json.dumps(build_politician_profile(sys.argv[i+1]), indent=2, ensure_ascii=False))
    elif "--compare" in sys.argv and len(sys.argv) >= 4:
        i = sys.argv.index("--compare")
        print(json.dumps(compare_two_politicians(sys.argv[i+1], sys.argv[i+2]), indent=2, ensure_ascii=False))
    elif "--analyze" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--analyze")
        text = sys.argv[i+1]
        pid = sys.argv[i+2] if len(sys.argv) > i+2 else "default"
        print(json.dumps(analyze_policy_phi7(text, pid), indent=2, ensure_ascii=False))
    else:
        print(f"{'Politician':25s} {'Meta':>6s} {'Rev':>6s} {'Mod':>6s} {'Lang':>6s} {'Zoom':>6s} {'Spir':>6s} {'Quan':>6s} {'Avg':>6s}")
        print("-" * 75)
        for pid in POLITICIANS:
            p = build_politician_profile(pid)
            s = p["phi7_scores"]
            avg = sum(s.values())/7
            print(f"{p['politician']:25s} {s['meta']:>5.1f} {s['reverse']:>5.1f} {s['modular']:>5.1f} {s['language']:>5.1f} {s['zoom']:>5.1f} {s['spiral']:>5.1f} {s['quantum']:>5.1f} {avg:>5.1f}")
