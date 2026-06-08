# 박찬대 되기 프로젝트 — 작업 로그 & TODO

> 본문: `박찬대-되기-프로젝트.html` (Section 01~08+)
> 철학 연결맵: `OrbitPrompt/boards/chan-dae-project.md`

---

## 현재 상태 (2026-06-08)

- **완료**: Section 01~08 (AI시대 정치인-시민 관계 모델까지)
- **🔴 정치 MCP v0.1 완성** — `dtslib-branch/mcp/` (6개 실무 툴 + 1개 메타 툴)
  - `server.py`로 명령 한 줄이면 정치인 업무 환경 전체 시뮬레이션 가능
  - `orchestrate` 툴 = 일인 오케스트레이션 방법론 자체를 MCP로 구현
- **마지막 커밋**: `6e2ee7d` — 박찬대 정치 MCP v0.1
- **SD카드 복사 완료**: `E:/mcp/political-mcp/`

## TODO (업데이트)

- [ ] Section 09+ 작업 재개 (컨텍스트 터짐으로 중단)
- [x] **Φ12 → 정치 시뮬레이션 MCP 포팅** — ✅ 완료 (6e2ee7d)
- [x] SD카드 로컬 서버에 박찬대 MCP 인스턴스 추가 — ✅ 완료
- [ ] Election MCP 연동 (`OrbitPrompt/prompts/election/`)
- [ ] GitHub 공개 레포 설정 (dtslib-branch/mcp/ → 공개)
- [ ] 정치인 데이터 확장 (박찬대 외 2~3명 추가)

---

## 세션 로그

### 2026-06-08 — phone_aider(DeepSeek) + Claude(Sonnet) 병렬 세션

#### 👤 Claude (형/PC 관제탑)

**완료한 것**
1. Section 08 "AI 시대 정치인-시민 관계" 완성 및 커밋 (`7ec61ca`)
   - 핵심 명제: "AI 시대에 시민은 하나의 개인 연구소가 되고, 정치인은 그 연구 결과를 도시와 제도 위에 꽂아볼 수 있는 아바타이자 파트너가 된다."
2. `chan-dae-worklog.md` 생성 → dtslib-branch에 작업 로그 체계 확립
3. `OrbitPrompt/boards/chan-dae-project.md` → 연결맵 형태로 정리 + Φ드라이버 포팅 맵 추가

---

#### 🤖 DeepSeek (phone_aider/폰)

**완료한 것**

1. **ENDPOINT 선형 판단 모델 v0.1~v0.4** — `~/OrbitPrompt/engine/`
   - classifier/sklearn/ONNX 파이프라인
   - 68K 샘플, F1 0.901
   - → 박찬대 정책 판단 엔진에 응용 가능

2. **WC2026 축구 예측 MCP** — `~/OrbitPrompt/football-model/mcp/`
   - `db.py` / `scraper.py` / `model.py` / `server.py` 전부 구현
   - Wikipedia FIFA랭킹 + GitHub 3332경기 실수집 (초기 하드코딩 → 실데이터 교체)
   - ELO 실제 계산 (K=32)
   - **`server.py`** 에 MCP 툴 `parksy_mcp_football_predict` 구현 완료
   - 3레이어 비교: **Φ12 vs Φ5 vs ELO baseline**
   - 10,000회 MC 시뮬레이션 완료
   - 케이스 스터디 웹페이지 커밋 (`acbf05d`)
   - `wc2026_prediction_data.json` 저장 (실제 결과 비교용)
   - 7드라이버 모두 실제 경기 데이터 기반으로 전환 (초기 하드코딩 수정)

3. **OrbitPrompt 랜딩 5개 카테고리 필터** 추가

4. **SD카드(E:/mcp/) MCP 복사** 완료 — 로컬 서버 운영 기반

5. **MANIFEST.md** — "축구 = 철학의 동사" 문서화

**박씨 확정 방향**
- MCP = 엔드 프로덕트 (출판 아님 — GitHub 공개 레포 배포)
- SD카드 로컬 서버 운영 → YouTube 반응 좋은 것만 Railway 백업
- GitHub 공개 레포 = 구독자 각자 로컬 설치

**Φ12 → 정치 MCP 포팅 근거**
- 축구: 48팀 × 7드라이버 × 10,000 MC = WC2026 예측
- 정치: N명 정치인 × 7드라이버 × 시뮬레이션 = 여론/정책 분석
- 구조 동일, 데이터 소스만 교체 (경기결과 → 발언/법안/지지율)
- Φ드라이버 server.py 툴 이미 구현됨 → 같은 패턴으로 정치 MCP server.py 작성 가능

---

#### ★ DeepSeek 정치 MCP 구현 완료 (6e2ee7d)

박씨가 Perplexity와 회의하면서 "일인 오케스트레이션 방법론 자체가 MCP"라고 한 개념을 코드로 구현.

**구현 파일:**
```
dtslib-branch/mcp/
├── phi7_political.py    — 7드라이버 정치 버전 (발언일관성/위기대응/정책조합/프레이밍/스케일링/모멘텀/변수중첩)
├── model.py             — Φ-I-C-K-P-7AXIS 통합 분석 (Φ5+Φ7=Φ12)
├── server.py            — MCP stdio 서버 (6개 실무 툴 + orchestrate 메타 툴)
├── db.py                — 정치인 데이터 저장소 (향후 scraper 연동)
├── political_data.json  — 박찬대 프로필 데이터
└── README.md            — 방법론 문서화
```

**6개 실무 툴:**
1. `policy_brief` — 정책 브리핑 + Φ드라이버 전략
2. `policy_analyze` — Φ7축 분석 + 정책 도입 영향 시뮬레이션
3. `message_draft` — 대외 발언/논평 초안 (4가지 톤)
4. `decision_check` — 안건 검토 + 리스크 분석 + 판결
5. `local_agenda` — 지역구 의제 트래킹 + Φ드라이버 우선순위
6. `press_release` — 보도자료 자동 작성

**★ 메타 툴 `orchestrate`:**
- 이 MCP 자체의 설계 철학을 반환
- 3층 구조(OrbitPrompt→dtslib-branch→현실실험)
- 4개 에이전트(박씨/Perplexity/DeepSeek/Claude) 역할 정의
- 3개 배포 채널(GitHub/SD카드/Railway)
- "사고방식이 도구가 되는 순간" 명시화

**핵심 통찰 (형 카운터 #002 반영):**
- MCP 자가실행: 박씨 없이 `server.py` 한 줄로 누구든 정치인 업무 환경 체험
- 역방향 유통: GitHub 공개 → 정치인이 찾아오는 구조
