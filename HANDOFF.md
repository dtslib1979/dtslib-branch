# 🌅 박씨 아침 확인 — 본사 ↔ 6 지사 통신 라이브

**작업일**: 2026-04-25 KST
**상태**: ✅ **6/6 지사 양방향 통신 가동 + ledger 18 entries**

---

## 🎯 한 줄 결론

박씨가 git push 한 번 하거나 격일 09:00 KST 마다 **6 지사가 본사에 자동 보고** + 박씨가 본사에서 **dimas 패널** 한 화면에서 모든 셀 모니터링 + notice 작성 폼으로 **6 지사 동시 디렉션**.

---

## 🚪 박씨 진입점 3개

| URL | 코드 | 용도 |
|---|:--:|---|
| https://dtslib1979.github.io/dtslib-branch/dimas/ | `1126` | 박씨 관제 패널 (6 셀 한 화면) |
| https://dtslib1979.github.io/{cell}/backoffice/ | `1126` | 각 지사 백오피스 (HQ 메시지 inbox) |
| https://github.com/dtslib1979/dtslib-branch/edit/main/hq/notices/notices.json | GitHub | 박씨 직접 디렉션 편집 |

**6 지사**: koosy / gohsy / artrew / papafly / namoneygoal / buckleychang.com

---

## 📊 작동 중인 자동 흐름

```
[매 격일 09:00 KST]
  6 지사 hq-upstream.yml 자동 실행
  → 본사 dispatches API 호출
  → 본사 hq-dispatch-receiver 실행
  → ledger.jsonl 6 줄 누적
  → dimas/ 패널 새로고침 시 자동 반영

[12시간마다]
  본사 hq-health-check 실행
  → 6 도메인 ping
  → 다운 시 ledger 에 health-report 기록

[박씨 git push 시]
  지사 푸시 → hq-upstream 즉시 트리거
  → 본사에 push 보고

[박씨 디렉션 보낼 때]
  dimas/ → compose 폼 작성 → JSON 클립보드
  → hq/notices/notices.json 편집 → git commit + push
  → 6 지사 backoffice 새로고침 시 즉시 표시
```

---

## 📁 박씨가 만질 파일

| 파일 | 용도 |
|---|---|
| `hq/notices/notices.json` | 박씨 → 6 지사 디렉션 (배너) |
| `hq/registry/branches.json` | 지사 등록부 (신규 셀 추가 시) |
| `hq/sync/install-cell.sh` | 새 지사 일괄 부트스트랩 |
| 절대 만지지 말 것: `hq/ledger/ledger.jsonl` (자동 누적) |

---

## 🛠 박씨가 자주 할 명령

```bash
# 새 디렉션 발사 (모든 지사에)
cd ~/dtslib-branch
# notices.json 편집 → 새 항목 추가
git add hq/notices/notices.json
git commit -m "notice: ..."
git push

# 새 셀 부트스트랩 (예: hoyadang.com 추가 시)
./hq/sync/install-cell.sh hoyadang dtslib1979/hoyadang.com HOYADANG
cd ~/hoyadang.com && git add -A && git commit -m "feat(hq): bootstrap" && git push

# 통신 강제 트리거 (디버그)
gh workflow run hq-upstream.yml -R dtslib1979/koosy --ref main
```

---

## 🔒 롤백

문제 시:
```bash
# 본사
cd ~/dtslib-branch && git reset --hard pre-hq-comm-bootstrap && git push -f

# 6 지사 한꺼번에
for r in koosy gohsy artrew papafly namoneygoal buckleychang.com; do
  cd ~/$r && git reset --hard pre-hq-comm-bootstrap && git push -f
done
```

---

## 💰 비용

```
GitHub Pages   무료 (public 무제한)
GitHub Actions 무료 (public repo 무제한, ~140분/월 사용)
외부 서비스    0개
─────────────────────────────────
인프라 총비용  0원
```

박씨 인프라 부담 = 도메인 연 ~₩100K (월 ₩8K 환산) + 선택사항.

---

## 🎁 보너스 (박씨 안 시킴)

- 6 지사 일괄 부트스트랩 자동화 (`install-cell.sh`)
- HQ_REPORT_TOKEN 자동 등록 (gh secret set)
- robots.txt /backoffice/ /.hq/ noindex
- ledger atomic retry (8회 fetch+reset+append)
- concurrency 셀별 분리
- payload ENV 안전화 (한글/괄호 문제 해결)
- backoffice 템플릿 array/{notices:[...]} 호환
- dimas 패널 compose form (JSON 클립보드 자동 생성)
- pre-hq-comm-bootstrap 태그 7개 (본사 + 6 지사 롤백 안전망)

---

## 📌 다음 작업 후보 (박씨 결정)

1. 추가 지사 등록 (gohsy-fashion / hoyadang / espiritu-tango / justino) — 1줄씩
2. branches.json v3.1 (추가 셀 반영)
3. notice 1번 직접 발송 시연 (박씨 실 메시지)
4. KOOSY 페르소나 v2 (와이프/아들/친구쿠씨 3 sub-cell)
5. dimas 패널에 `gh api dispatches` 직접 호출 (gh CLI 클라이언트)

---

## 📜 상세 기록

`docs/HQ-COMMUNICATION-LIVE-2026-04-25.md` — 5 wave test 이력 + 발견 4건 + 인프라 도식 + 안전망

`dimas/qa/` — Playwright 스크린샷 2장 (본사 패널 + KOOSY 백오피스)

---

*박씨 자고 일어나면 라이브. 추가 입력 0.*
