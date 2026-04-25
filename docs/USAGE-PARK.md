# 📖 박씨 사용법 — 인큐베이터 본사 운영

> **원칙**: 통제하지 않는다. 간접 고용한 친구/캐릭터가 램프업하는 서사를 콘텐츠화한다.

---

## 🎯 박씨가 하는 5가지 일

| 일 | 얼마나 자주 | 어디서 | 얼마 걸림 |
|---|---|---|:--:|
| 1. 아침 모니터링 | 매일 | https://dtslib1979.github.io/dtslib-branch/dimas/ | 30초 |
| 2. "이런 거 있어요" 알림 | 주 1~2회 | notices.json 편집 | 2분 |
| 3. 코워커 콘텐츠 업로드 | 수시 | 해당 지사 레포 | 5분 |
| 4. 서사 콘텐츠화 | 월 1~2회 | ledger → 블로그/방송 | 30분 |
| 5. 졸업 시키기 | 연 1~2명 | ownership 이관 | 10분 |

---

## 1️⃣ 아침 모니터링 (30초)

1. https://dtslib1979.github.io/dtslib-branch/dimas/ 열기
2. 코드 `1126` 입력
3. 6 셀 카드 확인 → online / 마지막 commit / time-ago
4. 끝.

→ 격일 09:00 KST 에 지사가 자동 보고. 박씨는 **읽기만** 함.

---

## 2️⃣ "이런 거 있어요" 알림 (2분)

코워커한테 "이런 게 있다" 정도 알려줄 때.
**명령 아님. 정보 공유만.**

### 방법 A: dimas 패널에서 (추천)

1. dimas 패널 하단 `COMPOSE NOTICE` 폼
2. 제목/내용/대상 지사(또는 ALL) 입력
3. `JSON 생성 → 클립보드 복사` 클릭
4. `QUICK ACTIONS → notices.json 편집` 클릭
5. 파일에 JSON 붙여넣기 → git commit → push
6. 끝. 6 지사 backoffice 에 즉시 표시됨.

### 방법 B: 터미널에서 직접

```bash
cd ~/dtslib-branch
# hq/notices/notices.json 편집 → 새 항목 추가
git add hq/notices/notices.json
git commit -m "notice: 내용"
git push
```

---

## 3️⃣ 코워커 콘텐츠 업로드 (5분)

코워커가 뭔가 만들어 오면 박씨가 해당 지사 레포에 올려준다.
(코워커는 자기 이름으로 올리는 경험만 함. 실제 git 작업은 박씨)

```bash
# 예: koosy 에 블로그 글 올림
cd ~/koosy
# 파일 추가/편집
git add .
git commit -m "feat: 새 글 by 쿠씨"
git push
```

→ `hq-upstream.yml` 이 push 감지 → 본사에 즉시 보고.
→ dimas 패널 새로고침 시 time-ago 갱신됨.

---

## 4️⃣ 서사 콘텐츠화 (월 1~2회, 30분)

**이게 박씨 진짜 수익원.**
코워커의 램프업 과정이 곧 콘텐츠.

```bash
# ledger 전체 읽기
cat ~/dtslib-branch/hq/ledger/ledger.jsonl

# 특정 지사만
grep '"cell":"koosy"' ~/dtslib-branch/hq/ledger/ledger.jsonl

# 또는 git log 로 실제 커밋 추출
cd ~/koosy
git log --reverse --oneline
```

### 서사 추출 → 콘텐츠 변환

- 코워커 1명의 3개월 ledger → 블로그 1편 ("쿠씨가 0에서 블로그 시작하기")
- 6 지사 1개월 전체 → 방송 1편 ("프랜차이즈 길드 성장기")
- 졸업생 전체 이력 → 책 1권 ("내 친구가 자립한 과정")

헌법 제1조: **레포는 소설이다.** ledger = 원고.

---

## 5️⃣ 졸업 시키기 (연 1~2명)

코워커가 자립 가능해지면:

```bash
# 1. 해당 지사 레포 ownership 이관
gh api -X POST repos/dtslib1979/koosy/transfer -f new_owner=koosy_user

# 2. 본사 branches.json 에서 제거 (또는 status: "graduated" 로 변경)
# hq/registry/branches.json 편집

# 3. 졸업 notice 발사
# "쿠씨 자립 축하! 인큐베이터 졸업."

# 4. dimas 패널에서 카드 제거됨
```

### 졸업 기준 (박씨 판단)
- 코워커가 본인 콘텐츠 아이디어를 스스로 냄
- 코워커가 GitHub/도메인 운영법 이해
- 박씨 없이 한 달 이상 운영 가능

---

## 🆕 새 코워커 온보딩 (1명 추가 시)

```bash
cd ~/dtslib-branch

# 1. 레포 생성 (예: hoyadang)
gh repo create dtslib1979/hoyadang --public

# 2. 부트스트랩 (install-cell.sh 가 다 해줌)
./hq/sync/install-cell.sh hoyadang dtslib1979/hoyadang HOYADANG

# 3. 레포에서 push
cd ~/hoyadang
git add -A && git commit -m "feat(hq): bootstrap"
git push

# 4. branches.json 에 추가
# hq/registry/branches.json 편집
```

끝. `HQ_REPORT_TOKEN` 자동 등록됨. 다음 격일 09:00 KST 부터 자동 보고.

---

## 🚨 절대 하지 말 것

- ❌ 코워커한테 "매출 보고해라" 요구 — 통제 모델 아님
- ❌ "품질 감사" 자동화 — 인큐베이터는 감시 안 함
- ❌ 로열티/과금 로직 구현 — 수익은 박씨의 콘텐츠화에서 나옴
- ❌ `git reset --hard` — 헌법 제2조 4대 원칙 위반 (반대 분개만)
- ❌ `hq/ledger/ledger.jsonl` 직접 편집 — 자동 누적 파일

---

## 🔄 롤백 (문제 발생 시)

```bash
# 본사
cd ~/dtslib-branch && git reset --hard pre-hq-comm-bootstrap

# 6 지사 한꺼번에
for r in koosy gohsy artrew papafly namoneygoal buckleychang.com; do
  cd ~/$r && git reset --hard pre-hq-comm-bootstrap && git push -f
done
```

---

## 📞 긴급 연락

- dimas 패널에서 ❌ 카드 → 해당 지사 레포 Actions 확인
- `gh workflow run hq-upstream.yml -R dtslib1979/<cell> --ref main` 으로 강제 트리거
- 계속 실패 → HANDOFF.md 9번 섹션 롤백 절차

---

*박씨는 콘텐츠 만드는 사람. 시스템은 자동으로 돌아가게 설계됨.*
