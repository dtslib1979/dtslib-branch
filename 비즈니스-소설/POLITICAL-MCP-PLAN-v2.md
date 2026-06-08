# 슬롯형 AI 정치 인프라 모델 — 개발 계획서 v2.0

> 작성: 2026-06-08
> v1 대비: 코드 구현 완료 (0줄 → 실제 작동)
> MCP: OrbitPrompt/political-mcp/server.py ← 지금 돌아감

---

## 모델 정의

이건 "박찬대를 만드는 프로젝트"가 아니다.
**시민이 AI로 정치 인프라를 만들고, 정치인이 그 인프라를 쓰는 게임이다.**

기존 AI 정치 이용 = AI를 정치 도구로
이 모델 = 시민이 AI로 인프라를 만들고 정치인이 그 인프라를 씀

방향이 반대다. 같은 리그가 아니다.

---

## 슬롯 구조

```
Layer 1 — 이름 슬롯 (언제든 교체)
  현재: 박찬대 (Episode 02 샘플)
  교체 가능: 다른 정치인 / 총장 / 재단 이사장 / 협동조합 리더

Layer 2 — 도시·의제 슬롯 (언제든 교체)
  현재: 인천 / AI 리터러시 / 인하대 / 노인·약자
  교체 가능: 서울 은평구 / 부산 / 교육청 / 사회적기업

Layer 3 — 협업 슬롯
  채우는 시점: 상대가 먼저 DM 올 때
```

---

## 현재 자산 (전부 구현 완료)

| 자산 | 상태 | 위치 |
|------|------|------|
| Φ드라이버 7축 철학 | ✅ | OrbitPrompt/docs/ |
| football-model MCP | ✅ | OrbitPrompt/football-model/mcp/ |
| **정치 MCP server.py** | ✅ **작동 확인** | OrbitPrompt/political-mcp/ |
| **analyze_politician 툴** | ✅ **실행됨** | political-mcp/server.py |
| **compare_policy 툴** | ✅ **실행됨** | political-mcp/server.py |
| **simulate_election 툴** | ✅ **실행됨** | political-mcp/server.py |
| **rank_politicians 툴** | ✅ **실행됨** | political-mcp/server.py |
| 삼각 실행 루프 방법론 | ✅ | OrbitPrompt/docs/TRIANGULAR-STAFF-METHOD.md |
| 박찬대 되기 프로젝트 HTML | ✅ Section 01~08 | dtslib-branch/비즈니스-소설/ |

**코드 0줄 → 없음. 전부 돌아간다.**

---

## MCP 실행 결과 샘플

### analyze_politician("박찬대")
```json
{
  "phi12_strength": 70.8,
  "axes_analysis": {
    "meta":     "발언 일관성 72/100",
    "reverse":  "위기 대응 68/100",
    "modular":  "정책 패턴 75/100",
    "language": "수사력 80/100",
    "zoom":     "의제 집중 70/100",
    "spiral":   "성장 궤적 74/100",
    "quantum":  "이변 가능성 55/100"
  }
}
```

### rank_politicians()
```
1위 이재명  Φ12: 77.9
2위 박찬대  Φ12: 70.8
3위 조국    Φ12: 57.0
4위 한동훈  Φ12: 47.7
```

---

## 역방향 유통 전략

GitHub 공개 → 손 뗀다 → 커뮤니티가 퍼뜨린다 → 보좌관이 DM 온다

```
박씨 → 정치인  (X) 전통 로비
정치인 → 박씨  (O) 역방향 유통
```

SD카드 E:/mcp/ = 24/7 로컬 서버
GitHub 퍼블릭 = 역방향 유통 출발점
Railway = DR 백업 (PC 죽을 때만)

---

## 갤러리 카테고리 (인지과학 4분류)

| | 카테고리 | 포함 |
|--|---------|------|
| 🎯 | THINK | 축구 MCP, **정치 MCP**, 금융 모델 |
| ✍️ | MAKE | Chalkboard, PWA, Editorial, 박찬대 HTML |
| 🔬 | DRAW | Dataset, Identity Engine |
| 📐 | FRAME | Φ드라이버, PHL, 백서, 삼각실행루프 |

---

## 삼각 실행 루프

```
박씨 (의사결정)
  → DeepSeek (구현 보좌관)
    → Claude (감사관) → counter.md 커밋
      → DeepSeek가 counter.md 읽음
        → 다음 답변 수정 → 루프 반복
```

레포 = 기억. 컨텍스트 터져도 팀 안 죽는다.

---

## 포지셔닝

> "나는 AI 시대 정치/리더십 인프라를 만드는 사람이다.
> 첫 번째 슬롯이 박찬대 Episode 02였을 뿐이다.
> 코드는 GitHub에 있다. 찾아오면 된다."

---

## 다음 STEP

- [ ] GitHub 퍼블릭 레포 생성 (orbitprompt-political-mcp)
- [ ] 실데이터 연결 (법안 투표 API / 국회 회의록)
- [ ] 두 번째 슬롯 (Episode 03 후보 결정)
