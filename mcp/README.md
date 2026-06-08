# 박찬대 정치 MCP — Φ-I-C-K-P-7AXIS Political Analysis

> **사고방식이 도구가 되는 순간**

## 개요

이 MCP는 **Φ-I-C-K-P-7AXIS 12차원 철학 모델**을 정치인·정책 분석에 적용한 구현체다.
OrbitPrompt(철학) → dtslib-branch(사례·백서) → 현실 실험(인천/인하대)으로 이어지는
**「사고방식 → 도구화 → 배포」 루프의 2단계**에 해당한다.

## 구조

```
mcp/
├── server.py            ★ MCP 서버 (stdio protocol, 6+1 툴)
├── model.py             Φ-I-C-K-P-7AXIS 정치 분석 모델
├── phi7_political.py    7드라이버 정치 버전 (핵심 엔진)
├── db.py                정치인 데이터 저장소
├── political_data.json  DB 파일 (자동 생성)
└── README.md            이 문서
```

## 철학: Φ-I-C-K-P-7AXIS

| Φ드라이버 | 축구 MCP (원본) | 정치 MCP (포팅) |
|-----------|----------------|----------------|
| Meta | 전술 일관성 | 발언 일관성 (과거 vs 현재 입장) |
| Reverse | 회복력 | 위기 대응력 (스캔들·역전 시나리오) |
| Modular | 선취점 후 승률 | 정책 모듈 조합력 (공약 패키지) |
| Language | 정체성 | 프레이밍/수사 전략 (메시지 구조) |
| Zoom | 빅매치 승률 | 중앙↔지역 스케일링 (국정↔지역구) |
| Spiral | 후반 상승폭 | 정치 사이클/이슈 증폭 (모멘텀) |
| Quantum | Upset rate | 변수 중첩/예측불가 (다중 이해관계) |

## 툴 목록

| 툴 | 설명 | 입력 |
|----|------|------|
| `policy_brief` | 정책 브리핑 + Φ드라이버 전략 | politician, topic |
| `policy_analyze` | Φ7축 정책 분석 + 영향 시뮬레이션 | politician, policy_text |
| `message_draft` | 대외 발언/논평 초안 | politician, topic, tone |
| `decision_check` | 안건 검토 + 리스크 분석 | politician, agenda, details |
| `local_agenda` | 지역구 의제 트래킹 (우선순위) | politician, region_focus |
| `press_release` | 보도자료 자동 작성 | politician, topic, key_message |
| `orchestrate` | ★ 메타: 방법론 전체 구조 | (없음) |

## 사용법

```bash
# 단일 툴 호출
echo '{"tool":"policy_brief","params":{"politician":"park_chan_dae","topic":"AI 리터러시"}}' | python3 server.py

# 정책 분석
echo '{"tool":"policy_analyze","params":{"politician":"park_chan_dae","policy_text":"..."}}' | python3 server.py

# 메시지 초안
echo '{"tool":"message_draft","params":{"politician":"park_chan_dae","topic":"...","tone":"positive"}}' | python3 server.py

# 안건 검토
echo '{"tool":"decision_check","params":{"politician":"park_chan_dae","agenda":"AI 리터러시","details":"예산 5억, 4회차 파일럿"}}' | python3 server.py

# 지역 의제
echo '{"tool":"local_agenda","params":{"politician":"park_chan_dae","region_focus":"인천"}}' | python3 server.py

# 보도자료
echo '{"tool":"press_release","params":{"politician":"park_chan_dae","topic":"AI 리터러시","key_message":"..."}}' | python3 server.py

# 메타: 방법론 조회
echo '{"tool":"orchestrate","params":{}}' | python3 server.py
```

## 일인 오케스트레이션 방법론 (이 MCP의 메타 의미)

이 MCP는 단순한 코드가 아니다. 아래 방법론의 구현체다:

```
박씨 (정치인/판단자)
  ↕
Perplexity (정책 브리핑·구조화)
  ↕
DeepSeek (구현·MCP 코딩)   ← 이 MCP가 여기
  ↕
Claude (검증·카운터·레포)
  ↕
GitHub (배포·역방향 유통)
  ↕
정치인/시민 (사용자)
```

### 핵심 통찰

1. **MCP = 자가실행 도구** — 박씨 없이 누구든 `server.py` 실행으로 정치인 업무 환경 체험
2. **GitHub = 역방향 유통** — 시민→정치인이 아니라 정치인→시민 동선
3. **Φ드라이버 = 재사용 가능한 프레임** — 축구→정치로 포팅 가능, 다음엔 패션/교육/물류로 확장

## 참조

| 문서 | 위치 |
|------|------|
| 연결맵 | `OrbitPrompt/boards/chan-dae-project.md` |
| 작업 로그 | `dtslib-branch/비즈니스-소설/chan-dae-worklog.md` |
| Claude 검증 | `dtslib-branch/비즈니스-소설/chan-dae-counter.md` |
| 백서 | `dtslib-branch/비즈니스-소설/박찬대-되기-프로젝트.html` |
| 원본 MCP | `OrbitPrompt/football-model/mcp/` |
