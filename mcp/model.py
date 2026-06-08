#!/usr/bin/env python3
"""
model.py — Φ-I-C-K-P-7AXIS 모델 (v2: phi7_political 통합)

축구 MCP(model.py)의 정치 포팅.
Φ7 7축이 전부. Φ5는 제거 (일반론으로 희석 방지).

레이어 단순화:
  Φ7 = 7드라이버 동적 점수 (데이터 기반) — THIS IS ALL WE NEED
"""

from phi7_political import phi7_profile, phi7_cross, phi7_policy_impact, phi7_strategy, calc_phi7_scores, POLITICIANS

# Φ12 = Φ7 (단일 레이어로 통일)
def calc_phi_12(politician_id: str) -> dict:
    p = phi7_profile(politician_id)
    return {
        "politician": p["politician"],
        "id": politician_id,
        "phi7_scores": p["phi7_scores"],
        "phi7_average": p["phi7_average"],
        "grade": p["grade"]
    }

if __name__ == "__main__":
    import sys, json
    if "--phi12" in sys.argv and len(sys.argv) >= 3:
        i = sys.argv.index("--phi12")
        print(json.dumps(calc_phi_12(sys.argv[i+1]), indent=2, ensure_ascii=False))
    elif "--list" in sys.argv:
        for pid in POLITICIANS:
            r = calc_phi_12(pid)
            s = r["phi7_scores"]
            print(f"{r['politician']:20s} Φ7:{r['phi7_average']:>5.1f} 등급:{r['grade']}  "
                  f"M:{s['meta']} R:{s['reverse']} Md:{s['modular']} L:{s['language']} "
                  f"Z:{s['zoom']} Sp:{s['spiral']} Q:{s['quantum']}")
    else:
        print("--phi12 <politician> | --list")
