# FLD OS Justification Whitepaper — 이론에서 구현까지

> **FLD (Fiction Ledger Design) OS** — HQ OS v3.0 헌법을 1,700라인 코드로 현실화한 기록

---

## 1. 선언 — "주고 싶어도 못 주는 공장"

HQ OS 백서는 말했다: *"교육은 실패한다. 시스템은 반복된다. 인간은 흔들린다. 공장은 흔들리지 않는다."*

FLD OS는 이 선언을 **5-State Ledger Machine**으로 구현했다.

| 백서 원리 | FLD OS 구현 | 증빙 |
|-----------|------------|------|
| "정책(Policy)이 판단한다" | `transition()` 가드: 4개 전이 조건 + 10항목 점수 | `ledger.py:125-150` |
| "원장(Ledger)이 남는다" | JSONL append-only ledger + history[] 배열 | `ledger.py:29-51` |
| "결정모드(Decision Mode)가 작동한다" | 5-state machine: Seed→Scenario→Candidate→Pilot→Protocol | `ledger.py:125-151` |
| "PR과 배포가 흐른다" | MCP SSE 서버 (port 8090) + Phone MCP Bridge | `fld_mcp_sse.py` + `phone_mcp_bridge.py` |

---

## 2. Control Plane → 5-State Machine

백서의 Control Plane은 `transition()` + `score_item()` 으로 실현되었다.

### 2.1 상태 전이 조건 (transition.py의 Guard Clause 구현)

```python
# 백서 "Policy가 판단한다" → 코드화된 전이 조건
if to_state == "scenario" and not item.raw_source:
    raise ValueError("Seed→Scenario 실패: raw_source 없음")    # Article 2 - Audit is Law
if to_state == "candidate" and not item.account:
    raise ValueError("Scenario→Candidate 실패: 계정군 미분류")   # Article 3 - Central Control
if to_state == "pilot" and item.score < 30:
    raise ValueError(f"Candidate→Pilot 실패: 점수 {item.score} < 30")  # Article 1 - Safety First
if to_state == "protocol" and not item.links:
    raise ValueError(f"Pilot→Protocol 실패: 자산 링크 없음")    # Article 5 - Cost is Reality
```

### 2.2 10항목 점수 엔진 (백서 Decision Modes 구현)

| 모드 | 점수 항목 | 점수 범위 |
|------|----------|----------|
| Physical (인간 판단) | immediacy, evidence | 2~10 |
| RAG (문서 기반) | maintainability, log_value | 2~10 |
| LLM (창작/요약) | deployability, mcp_potential | 2~10 |
| Ontology (규칙 엔진) | mobile_fit, reusability, revenue_potential, brand_fit | 4~20 |

**실제 평가 사례: NYU 드랍아웃 셰프 IP 발굴**
```
immediacy: 5/5  — 지금 바로 YouTube IP 전략 수립 가능
revenue_potential: 5/5 — 식당+유튜브 직결
evidence: 5/5 — 실제 식당+NYU 스토리 존재
→ 총점 45/50 (상위 90%)
```

---

## 3. Data Plane → JSONL Ledger + HQ 양방향 동기화

백서의 Data Plane은 두 개의 장부로 실현되었다.

### 3.1 FLD Ledger (app-startup ledger)

```jsonl
{"id":"FLD-1779797358-48d507", "state":"protocol", "score":45, 
 "account":"person", "history":[
   {"state":"seed","by":"system"},
   {"state":"scenario","by":"user"},
   {"state":"candidate","by":"user"},
   {"state":"pilot","by":"user"},
   {"state":"protocol","by":"user"}
 ]}
```

### 3.2 HQ Ledger (transaction ledger)

```jsonl
{"id":"TXN-20260526-121357-122572","eventType":"fld_state_change",
 "actor":"user","cell":"person","status":"success"}
```

### 3.3 Sync Bridge 구조

```
FLD OS ledger.jsonl  ←→  HQ ledger.jsonl
      │                       │
      ▼                       ▼
  fld_state_change       cell_registered
  (FLD→HQ)               (HQ→FLD Seed 생성)
```

**E2E 검증 완료**: NYU Chef Seed→Scenario→Candidate→Pilot→Protocol 전이 → HQ TXN 발행 확인

---

## 4. Execution Plane → MCP 도구 + 폰 브릿지 + 자동 수집

백서의 "Workers, LLM, GitHub API"는 세 가지 실행 계층으로 구현되었다.

### 4.1 MCP SSE Server (port 8090)

| 도구 | 백서 대응 | 호출 예 |
|------|----------|---------|
| `fld_seed` | Article 2 - 기록 의무화 | `curl -X POST localhost:8090 -d '{"tool":"fld_seed",...}'` |
| `fld_scenario` | Decision Mode - Scenario 평가 | Seed→Scenario 전이 |
| `fld_candidate` | Article 4 - Human in the Loop | 점수 평가 포함 |
| `fld_pilot` | Article 1 - Safety First | score≥30 검증 |
| `fld_protocol` | Article 5 - Cost is Reality | links 필수 |
| `fld_score` | Ontology Mode | 10항목 50점 |

### 4.2 Phone MCP Bridge (SSH)

11개 분배 도구 연결 → FLD Protocol 상태 Item을 Telegram/YouTube/Naver/Tistory/Dischord로 자동 배포

```bash
fld distribute FLD-xxxxx.mp4 telegram   # 텔레그램 배포
fld phone status                        # 채널 상태 조회
```

### 4.3 Parksy Capture Auto-Ingest

로그 파일 생성 → 자동 Seed 등록 (inotify/폴링)

```
ParksyLog_20260526_174126.md
  → parksy_watcher.py parse
    → FLD Seed [person] NYU 드랍아웃 셰프 IP 발굴
      → score_item() → 45/50
        → transition() → protocol
          → hq_sync() → TXN-20260526-...
```

---

## 5. Termux:Widget 7-Pack — 모바일 운영

백서 "HQ는 죽지 않는 시스템" → 모바일에서 전부 조작 가능

| 위젯 | 백서 조항 | 기능 |
|------|----------|------|
| 01_capture | Article 2 - Audit is Law | 로그 수집 → Seed |
| 02_scenario | Decision Mode | Seed 목록 조회 |
| 03_ledger_post | Article 5 - Cost is Reality | 수동 Seed 등록 |
| 04_filter | Observability 원칙 | 상태/계정 필터 |
| 05_pilot_launch | Article 1 - Safety First | Candidate→Pilot |
| 06_logback | Audit Trail | 변경 이력 |
| 07_protocol_pack | Article 3 - Central Control | Protocol 자산화 |

---

## 6. 검증 결과 요약

| 항목 | 결과 |
|------|------|
| 총 코드 라인 | 1,682라인 (19개 파일) |
| 실제 FLD Item | 13개 (Seed 9 / Scenario 3 / Protocol 1) |
| 최고 점수 Item | NYU Chef 45/50 |
| HQ 동기화 TXN | 20개 기존 + 1개 신규 (fld_state_change) |
| MCP 도구 | 10개 전부 응답 OK |
| 폰 연동 | SSH MCP Bridge 11개 도구 + file server 9999 |
| 상태 전이 검증 | Seed→Scenario→Candidate→Pilot→Protocol 전부 통과 |

---

## 7. Operational Constitution — 이행 증명

| 조항 | 요구사항 | FLD OS 이행 |
|------|---------|-------------|
| Article 1 - Safety First | canary deploy mandatory | Candidate→Pilot score≥30 조건 |
| Article 2 - Audit is Law | 모든 변경 ledger 기록 | history[] 배열 + HQ TXN 동기화 |
| Article 3 - Central Control | policy 위반 PR 거부 | transition() guard clause |
| Article 4 - Human in the Loop | AI는 실행자 | score_item()에 인간 평가 반영 |
| Article 5 - Cost is Reality | 각자 비용 부담 | account별 통계 + HQ billing 연동 |

---

> **"사람을 바꾸려 하지 않는다. 사람이 바뀐 것처럼 행동하게 만드는 판을 만든다."**
>
> FLD OS는 이 하나의 문장을 위해 1,682라인을 썼고,
> 5-state machine + 10-criteria scoring + 2-way HQ sync + 7 mobile widgets로 증명했다.
>
> *Version: 1.0 | Built: 2026-05-26 | Commit: 5d35428*
