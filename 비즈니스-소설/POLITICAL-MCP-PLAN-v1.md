# 슬롯형 AI 정치 인프라 모델 — 개발 계획서 v1.0

> 작성: 2026-06-08
> 작성자: Claude (삼각 실행 루프 감사관)
> 기반: 박씨↔DeepSeek↔Claude 세션 카운터 #001~#007 전체 반영

---

## 모델 정의

이건 "박찬대를 만드는 프로젝트"가 아니다.
**시민이 AI로 정치 인프라를 만들고, 정치인이 그 인프라를 쓰는 게임이다.**

기존 AI 정치 이용 (타겟 광고, 챗봇, 딥페이크) = AI를 정치 도구로
이 모델 = 시민이 AI로 인프라를 만들고 정치인이 그 인프라를 씀

방향이 반대다. 같은 리그가 아니다.

---

## 슬롯 구조

```
Layer 1 — 이름 슬롯
  현재: 박찬대 (Episode 02 샘플)
  언제든 교체 가능: 다른 정치인 / 총장 / 재단 이사장 / 협동조합 리더

Layer 2 — 도시·의제 슬롯
  현재: 인천 / AI 리터러시 / 인하대 / 노인·약자
  언제든 교체 가능: 서울 은평구 / 부산 / 교육청 / 사회적기업

Layer 3 — 협업 슬롯
  현재: 비어있음
  채우는 시점: 상대가 먼저 DM 올 때
```

박찬대가 안 쓰면 다음 슬롯에 꽂으면 된다.
형식이 살아있으면 슬롯은 언제든 교체된다.

---

## 현재 자산

| 자산 | 상태 | 위치 |
|------|------|------|
| Φ드라이버 7축 철학 | ✅ 완성 | OrbitPrompt/docs/ |
| football-model MCP | ✅ 완성 | OrbitPrompt/football-model/mcp/ |
| 삼각 실행 루프 방법론 | ✅ 문서화 | OrbitPrompt/docs/TRIANGULAR-STAFF-METHOD.md |
| 박찬대 되기 프로젝트 HTML | ✅ Section 01~08 | dtslib-branch/비즈니스-소설/ |
| 갤러리 카테고리 재설계 | ✅ 문서화 | OrbitPrompt/docs/GALLERY-CATEGORY-REDESIGN.md |
| **정치 MCP 코드** | ❌ 0줄 | ← 여기만 없음 |

---

## 실행 플랜

### STEP 1 — 정치 MCP 구현 (이번 세션)

football-model/mcp/server.py 구조 그대로 복사.
데이터 소스만 교체: 경기 결과 CSV → 법안 투표 + 발언 기록.

**툴 3개:**

```python
analyze_politician(name: str)
  → Φ드라이버 7축으로 정치인 해부
  → Meta(발언 일관성) / Reverse(위기 대응) / Modular(정책 패턴)
  → Language(수사 분석) / Zoom(의제 집중도) / Spiral(성장 궤적) / Quantum(이변 가능성)

compare_policy(policy_a: str, policy_b: str)
  → 두 정책 Φ드라이버 비교
  → 어느 축에서 차이 나는지 분석

simulate_election(candidate: str, region: str)
  → 지역 의제 + 후보 Φ점수 기반 시나리오 시뮬레이션
  → 3레이어 비교: Φ12 vs Φ5 vs 여론조사 baseline
```

**레포명:** `orbitprompt-political-mcp`
**공개:** GitHub 퍼블릭

---

### STEP 2 — 역방향 유통 (손 안 댄다)

GitHub 공개 후 건드리지 않는다.

경로:
```
GitHub 공개
  → 레딧 r/PoliticalDiscussion, r/AItools 자연 확산
  → 해커뉴스 Show HN 가능
  → 보좌관 / 연구원 "이거 뭐야?" DM
    → 이 시점에 박씨가 응답
```

박씨→정치인 동선 아님. 정치인→박씨 동선.
채널을 만드는 게 아니라 찾아오게 만든다.

---

### STEP 3 — 슬롯 채우기

DM 왔을 때 가져갈 것:
- MCP 데모 (server.py 실행 결과 스크린샷)
- 박찬대 프로젝트 케이스스터디 HTML
- Φ드라이버 철학 1페이지 요약

박씨 포지션:
> "나는 AI 시대 정치/리더십 인프라를 만드는 사람이다.
> 첫 번째 슬롯이 박찬대 Episode 02였을 뿐이다."

박찬대 안 쓰면 → 다음 슬롯.

---

### STEP 4 — 확장

```
두 번째 슬롯 (다른 도시/리더) → Episode 03
세 번째 슬롯 → Episode 04
언론 레퍼링 → 역방향으로 유명해짐
"인천형 AI 정치 참여 모델" 명명됨
```

---

## MCP 배포 전략

| 채널 | 역할 | 시점 |
|------|------|------|
| SD카드 E:/mcp/ | 로컬 서버 (24/7) | STEP 1 완료 즉시 |
| GitHub 퍼블릭 | 역방향 유통 출발점 | STEP 1 완료 즉시 |
| Railway | DR 백업 (PC 죽을 때만) | YouTube 반응 나올 때 |

구독자 = GitHub에서 각자 로컬 설치.
박씨가 서버 운영 안 해도 된다.

---

## 갤러리 카테고리 (OrbitPrompt 랜딩)

인지과학 기반 4분류로 교체:

| 카테고리 | 포함 | 현재 상태 |
|---------|------|---------|
| 🎯 THINK | 축구 MCP, 정치 MCP, 금융 모델 | 도메인 드릴다운 2단계 |
| ✍️ MAKE | Chalkboard, PWA, Editorial, 박찬대 HTML | Generator + 결과물 통합 |
| 🔬 DRAW | Dataset, Identity Engine | 추출·파싱 도구 |
| 📐 FRAME | Φ드라이버, PHL, 백서, 삼각실행루프 | 철학·방법론 |

---

## 삼각 실행 루프 (이 프로젝트 운영 방식)

```
박씨 (의사결정) → DeepSeek (구현) → Claude (감사/카운터)
                                          ↓
                              counter.md GitHub 커밋
                                          ↓
                              DeepSeek가 counter.md 읽음
                                          ↓
                              DeepSeek 다음 답변 수정
                                          ↑
                              루프 반복
```

레포 = 기억. 컨텍스트 터져도 팀 안 죽는다.

---

## 지금 당장 할 것

```
1. orbitprompt-political-mcp 레포 생성
2. football-model/mcp/server.py 복사
3. 정치 데이터 소스 연결
4. 툴 3개 구현: analyze_politician / compare_policy / simulate_election
5. GitHub 퍼블릭 공개
6. 손 뗀다
```

백서 섹션 추가는 STEP 1 이후다. 코드가 먼저다.
