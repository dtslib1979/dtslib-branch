# 🛡 HQ Communication LIVE — 본사 ↔ 6 지사 양방향 통신 가동

**활성 일시**: 2026-04-25 KST 오전
**프로토콜**: Franchise OS v1.0 + hqProtocolVersion 3.0
**범위**: koosy / gohsy / artrew / papafly / namoneygoal / buckleychang

---

## 1. 통신 메커니즘 작동 검증

### Wave Test 5회 결과

| Wave | 시각 | 6 지사 upstream | 본사 receiver | ledger 누적 |
|:--:|---|:--:|:--:|:--:|
| 1 | 01:07 | 6/6 ✅ | 0/6 (templates 비어있음) | 0 |
| 2 | 01:09 | 6/6 ✅ | 0/6 (workflow disabled) | 0 |
| 3 | 01:37 | 6/6 ✅ | 0/6 (한글 payload syntax err) | 0 |
| 4 | 01:39 | 6/6 ✅ | 1/6 (concurrency cancel) | 1 |
| **5 final** | **01:43** | **6/6 ✅** | **6/6 ✅** | **6** |
| **6 push trigger** | **01:48** | **6/6 ✅** | **6/6 ✅** | **6** |

**최종**: 18 ledger entries, 6 cells online.

### 발견 + 수정한 문제 4건

| # | 문제 | 수정 |
|:--:|---|---|
| 1 | `hq/sync/templates/` 비어있음 → PR 보낼 게 없음 | 3 템플릿 작성 |
| 2 | 본사 `hq-dispatch-receiver` `disabled_manually` | API 활성화 |
| 3 | payload 한글 + `(hq)` 괄호가 bash echo 에 직접 노출 → syntax error | `env: PAYLOAD_JSON` ENV 변수로 안전화 |
| 4 | concurrency `cancel-in-progress: false` 도 6 동시 트리거 시 5 cancel | group 을 `cell` 별로 분리 |
| 5 | ledger.jsonl 동시 append → rebase merge conflict | fetch + reset + append + push 8회 atomic retry |

---

## 2. 인프라 구조

```
┌────────────────────────────────────────────────────────────┐
│  박씨 (DIMAS)                                               │
│  https://dtslib1979.github.io/dtslib-branch/dimas/         │
│  (noindex · code 1126/dimas)                               │
│                                                            │
│  · 6 셀 카드 한 화면                                        │
│  · ledger 최근 30건                                         │
│  · notice 작성 폼 (JSON 자동 생성 → 클립보드)              │
└────────────────────────────────────────────────────────────┘
                          ↑
                          │ git pull/push
                          ↓
┌────────────────────────────────────────────────────────────┐
│  본사 dtslib-branch                                         │
│  Franchise OS v1.0                                         │
│                                                            │
│  hq/registry/branches.json     6 cells 등록                 │
│  hq/sync/templates/            install 자료                 │
│  hq/sync/install-cell.sh       부트스트랩 자동              │
│  hq/sdk/dtslib-bridge.js       SDK v3.0                     │
│  hq/notices/notices.json       박씨 → 6 지사 디렉션          │
│  hq/ledger/ledger.jsonl        ERP 원장 (append-only)       │
│                                                            │
│  .github/workflows/                                         │
│    hq-dispatch-receiver.yml    셀별 concurrency · 8회 retry │
│    hq-sync-downstream.yml      템플릿 변경 시 PR 자동 발송   │
│    hq-health-check.yml         12시간 ping (격일 → 반일)     │
│    hq-billing-aggregate.yml    월 1회 집계                  │
│    hq-spawn-cell.yml           새 셀 생성                   │
│    hq-backup.yml / validate.yml                             │
└────────────────────────────────────────────────────────────┘
                          ↑                ↓
        repository_dispatch                GitHub PR
        (cell-report)                      (downstream)
                          ↑                ↓
┌────────────────────────────────────────────────────────────┐
│  6 지사 (전부 동일 install)                                  │
│                                                            │
│  .hq/manifest.json             cellId + hqProtocolVersion   │
│  .github/workflows/                                         │
│    hq-receiver.yml             HQ dispatch 수신             │
│    hq-upstream.yml             격일 09:00 + push 자동 보고  │
│  backoffice/index.html         표준 백오피스 (code 1126)    │
│  branch.json                   subscriptions[]              │
│  robots.txt                    /backoffice/ /.hq/ noindex   │
│  Secret HQ_REPORT_TOKEN        gh CLI 토큰 자동 등록         │
└────────────────────────────────────────────────────────────┘
```

---

## 3. 격일 보고 모델

| 워크플로우 | 주기 | 동작 |
|---|:--:|---|
| **hq-upstream.yml** (지사) | 격일 자정 UTC = **한국 09:00 KST** | cell-report dispatch |
| **+ push trigger** | git push main 시 | 즉시 보고 (옵션 트리거) |
| **hq-health-check.yml** (본사) | **12시간** (반일) | 6 도메인 ping |
| **hq-billing-aggregate.yml** (본사) | 월 1회 (1일) | 비용 집계 |

→ Actions 사용량 ~140분/월 (Free tier 2,000 분의 7%, public repo 무제한).

---

## 4. 박씨 평소 흐름

```
[격일 아침 09:00 KST]
  6 지사가 한꺼번에 cell-report dispatch
  → 본사 ledger.jsonl 6 줄 누적
  → 박씨 dimas/ 패널 새로고침 → 6 카드 "online" + 최신 commit hash

[박씨가 디렉션 발사할 때]
  dimas/ 패널 compose form
  → 대상 지사 선택 + 제목 + 내용
  → JSON 자동 생성 + 클립보드 복사
  → notices.json 편집 페이지로 이동 (Quick Action 버튼)
  → JSON 추가 → git commit → push
  → 6 지사 backoffice 화면에 즉시 표시

[지사가 git push 시]
  hq-upstream.yml 자동 트리거
  → 즉시 본사에 보고
  → ledger 추가 줄 + dimas/ 카드 timestamp 갱신
```

---

## 5. 6 지사 라이브 URL

| Cell | 공개 사이트 | 백오피스 (noindex) | 마지막 commit |
|---|---|---|:--:|
| **KOOSY** | https://koosy.kr | /backoffice/ | cf9fdf94 |
| **GOHSY** | https://dtslib1979.github.io/gohsy/ | /backoffice/ | df6fb22d |
| **ARTREW** | https://artrew.com | /backoffice/ | c48f130b |
| **PAPAFLY** | https://papafly.kr | /backoffice/ | 9446c87e |
| **NAMONEYGOAL** | https://namoneygoal.kr | /backoffice/ | 9bf1599d |
| **BUCKLEY** | https://buckleychang.com | /backoffice/ | 352e8dad |

**박씨 본사 관제**: https://dtslib1979.github.io/dtslib-branch/dimas/

**Access codes** (전부 동일):
- 본사 dimas: `1126` 또는 `dimas`
- 각 지사 backoffice: `1126` 또는 `{cell_id}` (예: koosy 는 `koosy`)

---

## 6. 비용 검증

| 항목 | 사용량 | 한도 | 비용 |
|---|---|---|:--:|
| GitHub Pages | 28레포 정적 | public 무제한 | **0원** |
| GitHub Actions | ~140분/월 | public 무제한 | **0원** |
| GitHub Storage | 1GB 미만 | 5GB 권장 | **0원** |
| 외부 서비스 | 0개 | — | **0원** |
| **인프라 총 비용** | | | **0원** |
| 도메인 (6개 .kr/.com) | 별도 | | 연 ~₩100K |
| GitHub Pro (선택) | 박씨 개인 | | 월 ~₩4K |

**박씨 인프라 부담 = 약 월 ₩12K** (Pro + 도메인 12분의 1).

---

## 7. 안전망 (롤백)

```bash
# 본사
cd ~/dtslib-branch && git reset --hard pre-hq-comm-bootstrap

# 각 지사 (예: koosy)
cd ~/koosy && git reset --hard pre-hq-comm-bootstrap
git push origin main --force-with-lease
```

태그 `pre-hq-comm-bootstrap` 이 본사 + 6 지사 전부에 찍혀 있음.

---

## 8. 추가 가능한 확장 (선택)

- **추가 지사 등록**: `./hq/sync/install-cell.sh <id> <repo> <NAME>` 한 줄로 부트스트랩
  - 후보: gohsy-fashion, gohsy-production, hoyadang.com, espiritu-tango, justino, hq, eae-univ
- **dispatch types 확장**: deploy-result, health-report, cost-report 이미 receiver 가 처리
- **branches.json v3.0 → v3.1**: 추가 지사 등록 시
- **dimas/ 패널 v2**: 메시지 자동 push (gh CLI 호출)

---

*Bootstrapped 2026-04-25 by Claude Opus 4.5 + 박씨*
*박씨 자고 일어나면 6 지사 매 격일 09:00 KST 자동 보고 시작.*
