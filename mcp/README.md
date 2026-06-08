# Φ-I-C-K-P-7AXIS 정치 MCP (보좌관 B2B)

> **Φ7 7축이 전부다 — 나머지는 없다.**

## v0.1 → v0.2 변경사항

| 항목 | v0.1 (문제) | v0.2 (수정) |
|------|------------|------------|
| 툴 구성 | 6개 중 5개가 일반 LLM 래퍼 | **Φ7 7축 기반 4개 툴** |
| Φ드라이버 | 1개 툴에만 사용 | **모든 툴이 Φ7 통과** |
| 타겟 | 일반 시민 | **의원실 보좌관 (B2B)** |
| 차별화 | 없음 (ChatGPT로 대체 가능) | **Φ7 데이터 분석 = 유일무이** |

## 구조

```
mcp/
├── phi7_political.py    ★ Φ7 7축 엔진 (데이터 기반 점수 계산)
├── server.py            MCP stdio 서버 (4개 툴 + 메타)
├── model.py             Φ7 단일 레이어 (Φ5 제거)
├── db.py                데이터 저장소 (향후 확장용)
└── README.md            이 문서
```

## 툴

| 툴 | 설명 | 보좌관 사용 시나리오 |
|----|------|-------------------|
| `phi7_profile` | 정치인 7축 프로필 | "이 의원 Φ7 등급이 어떻게 되나?" |
| `phi7_cross` | 두 정치인 Φ7 비교 | "우리 의원 vs 상대방, 어디가 우세?" |
| `phi7_policy` | 정책 Φ7 영향 예측 | "이 공약 내면 Φ7 점수 어떻게 바뀌나?" |
| `phi7_strategy` | Φ7 전략 리포트 | "이 의제, 어떻게 전개하는 게 최적?" |
| `orchestrate` | ★ 메타: 방법론 전체 | "이 MCP 자체가 뭔가?" |

## 사용법

```bash
# 정치인 프로필
echo '{"tool":"phi7_profile","params":{"politician":"park_chan_dae"}}' | python3 server.py

# 두 정치인 비교 (보좌관 B2B 핵심)
echo '{"tool":"phi7_cross","params":{"politician_a":"park_chan_dae","politician_b":"park_chan_dae"}}' | python3 server.py

# 정책 영향 예측
echo '{"tool":"phi7_policy","params":{"politician":"park_chan_dae","policy_text":"인천 AI 리터러시 4회차 파일럿..."}}' | python3 server.py

# 전략 리포트
echo '{"tool":"phi7_strategy","params":{"politician":"park_chan_dae","agenda":"AI 리터러시"}}' | python3 server.py

# 메타
echo '{"tool":"orchestrate","params":{}}' | python3 server.py
```

## 설계 철학

형(Claude) 카운터 #003 기반 재설계:

1. **Φ7이 전부다** — 일반 텍스트 생성/LLM 래퍼는 전부 제거. 모든 출력이 7축 점수의 직간접 함수.
2. **보좌관이 타겟** — "시민이 정치인 접신"이 아니라 "A의원실 보좌관이 B의원 분석용 B2B 도구"
3. **데이터 기반** — 정치인 데이터(발언/법안/경력/미디어)로 7축 점수 자동 계산. 수동 입력 없음.

## 연결

```
OrbitPrompt (Φ드라이버) → 이 MCP (정치 분석) → 보좌관 (B2B 사용)
                                        ↘ GitHub 공개 → 역방향 유통
```
