#!/usr/bin/env python3
"""
db.py — 정치 MCP 데이터 저장소

POLITICIANS DB 확장: 발언·법안·지지율 데이터 저장/조회
향후 scraper.py로 뉴스/여론 데이터 자동 수집 연동

Φ-I-C-K-P-7AXIS 정치 분석 모델의 데이터 레이어
"""

import json, os
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "political_data.json"

# ─── 기본 데이터 ──────────────────────────────────────────
DEFAULT_DATA = {
    "politicians": {
        "park_chan_dae": {
            "name": "박찬대",
            "party": "더불어민주당",
            "district": "인천 연수구",
            "position": "국회의원 · 원내대표",
            "education": "인하대 경영학과",
            "birth": "1965",
            "career": [
                "제21대·22대 국회의원",
                "더불어민주당 원내대표",
                "회계사",
                "인하대 경영학과"
            ],
            "keywords": ["AI", "인천", "물류", "돌봄", "경영", "회계사", "민주당"],
            "key_policies": [
                "AI 도시 인천 비전",
                "노인·약자 AI 리터러시",
                "인천 물류 허브",
                "지역 돌봄 인프라"
            ],
            "speeches": [
                {"date": "2026-05-15", "title": "AI 시대, 인천의 새로운 비전", "summary": "인천을 AI 도시로 전환하겠다는 비전 선언"},
                {"date": "2026-04-20", "title": "원내대표 취임사", "summary": "민주당 원내 협력과 견제 역할 강조"},
            ],
            "bills": [
                {"number": "12345", "title": "AI 리터러시 교육 지원법", "status": "발의"},
            ]
        }
    },
    "meta": {
        "version": "0.1.0",
        "updated": datetime.now().isoformat(),
        "source": "Φ-I-C-K-P-7AXIS 정치 MCP",
        "description": "OrbitPrompt 철학 → dtslib-branch 정치 MCP 데이터"
    }
}

def load_db() -> dict:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text(encoding="utf-8"))
    return dict(DEFAULT_DATA)

def save_db(data: dict):
    DB_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_politician(politician_id: str) -> dict:
    db = load_db()
    return db.get("politicians", {}).get(politician_id, {})

if __name__ == "__main__":
    if not DB_PATH.exists():
        save_db(DEFAULT_DATA)
        print(f"✅ DB 생성됨: {DB_PATH}")
    db = load_db()
    print(f"📊 DB 로드 완료: {len(db.get('politicians', {}))}명 정치인")
    for pid, info in db.get("politicians", {}).items():
        print(f"  {info['name']} ({info['party']}) — {info['district']}")
        print(f"    정책: {', '.join(info['key_policies'][:3])}")
