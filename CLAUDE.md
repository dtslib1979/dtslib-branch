# dtslib \uc5d0\uc774\uc804\ud2b8 \ud504\ub85c\ud1a0\ucf5c

---

## 헌법 제1조: 레포지토리는 소설이다

> **모든 레포지토리는 한 권의 소설책이다.**
> **커밋이 문장이고, 브랜치가 챕터이고, git log --reverse가 줄거리다.**

- 삽질, 실패, 방향 전환 전부 남긴다. squash로 뭉개지 않는다.
- 기능 구현 과정 = 플롯 (문제→시도→실패→전환→해결)
- 레포 서사 → 블로그/웹툰/방송 콘텐츠로 파생 (액자 구성)

### 서사 추출 명령

```bash
narrative-extract.py --repo .                    # 이 레포 줄거리
narrative-extract.py --repo . --format synopsis  # 시놉시스
narrative-extract.py --repo . --format blog      # 블로그 원고
narrative-extract.py --repo . --climax           # 전환점만
narrative-extract.py --all ~                     # 28개 레포 연작 인덱스
```

### 서사 분류

| 커밋 유형 | 서사 | 의미 |
|-----------|------|------|
| `feat:` / 기능 추가 | 시도 | 주인공이 무언가를 만든다 |
| `fix:` / 버그 수정 | 삽질 | 예상대로 안 됐다 |
| `migration` / 전환 | 전환 | 버리고 다른 길을 간다 |
| `rewrite` / v2 | 각성 | 처음부터 제대로 다시 한다 |
| `refactor:` | 성장 | 같은 일을 더 잘하게 됐다 |
| `docs:` | 정리 | 지나온 길을 돌아본다 |

---

## ⚙️ 헌법 제2조: 매트릭스 아키텍처

> **모든 레포지토리는 공장이다.**
> **가로축은 재무 원장(ERP)이고, 세로축은 제조 공정(FAB)이다.**

### 가로축: 재무 원장 (ERP 로직)

커밋은 전표다. 한번 기표하면 수정이 아니라 반대 분개로 정정한다.

| 회계 개념 | Git 대응 | 예시 |
|-----------|----------|------|
| 전표 (Journal Entry) | 커밋 | `feat: 새 기능 구현` |
| 원장 (General Ledger) | `git log --reverse` | 레포 전체 거래 이력 |
| 계정과목 (Account) | 디렉토리 | `tools/`, `scripts/`, `assets/` |
| 회계 인터페이스 | 크로스레포 동기화 | 명시적 스크립트/매니페스트 |
| 감사 추적 (Audit Trail) | Co-Authored-By | AI/Human 협업 기록 |

### 세로축: 제조 공정 (FAB 로직)

레포는 반도체 팹이다. 원자재(아이디어)가 들어와서 완제품(콘텐츠)이 나간다.

| 제조 개념 | 레포 대응 | 예시 |
|-----------|----------|------|
| BOM (자재 명세) | 의존성 + 에셋 목록 | `pubspec.yaml`, `package.json`, `assets/` |
| 라우팅 (공정 순서) | 파이프라인 스크립트 | 빌드→테스트→배포 순차 실행 |
| WIP (재공품) | 브랜치 + Queue | `claude/*` 브랜치, `_queue/` |
| 수율 (Yield) | 빌드 성공률 | CI 통과율, 테스트 커버리지 |
| MES (제조실행) | 자동화 스크립트 | 동기화, 추출, 배포 도구 |
| 검수 (QC) | 테스트 + 리뷰 | `tests/`, 체크리스트 |

### 4대 원칙

1. **삭제는 없다, 반대 분개만 있다** — `git revert`로 정정. `reset --hard` 금지.
2. **증빙 없는 거래는 없다** — 커밋 메시지에 이유와 맥락. 크로스레포 이동은 명시적 스크립트로.
3. **BOM 확인 후 착공한다** — 의존성/에셋 명세 먼저, 공정 순서 명시 후 실행.
4. **재공품을 방치하지 않는다** — WIP 브랜치와 큐는 정기적으로 소화한다.

### 교차점: JSON 매니페스트

가로축과 세로축이 만나는 곳에 JSON이 있다. 매니페스트는 공정 기록이자 거래 증빙이다.

```
app-meta.json      = 제품 사양서
state.json         = 공정 현황판
*.youtube.json     = 출하 전표
*-SOURCES.md       = 원자재 입고 대장
```

### Claude 자동 체크

| 트리거 | 체크 | 위반 시 |
|--------|------|---------|
| `git commit` 전 | 커밋 메시지에 이유/맥락 있는가 | "증빙 누락" 경고 |
| `reset --hard` 요청 | 반대 분개(revert) 가능한가 | 차단, revert 제안 |
| 새 파일/도구 추가 | BOM(package.json 등) 업데이트했는가 | "BOM 미갱신" 경고 |
| 세션 시작 | `git branch --no-merged main` WIP 확인 | 3개 이상이면 정리 권고 |
| 크로스레포 작업 | 동기화 스크립트/매니페스트 경유하는가 | "인터페이스 우회" 경고 |

> **코드를 짜는 게 아니라 공장을 돌리고 있다.**
> **다만 그 공장의 원장이 git이고, 라인이 파이프라인일 뿐이다.**

---


> \uc774 \ubb38\uc11c\ub294 Claude Code\uac00 dtslib-branch \ub808\ud3ec\uc9c0\ud1a0\ub9ac\uc5d0\uc11c \uc791\uc5c5\ud560 \ub54c \ub530\ub77c\uc57c \ud558\ub294 \uac00\uc774\ub4dc\uc785\ub2c8\ub2e4.

---

## 1. \ud504\ub85c\uc81d\ud2b8 \uac1c\uc694

### \ubaa9\uc801
AI \uc5c5\ubb34 \uc790\ub3d9\ud654 \ucee8\uc124\ud305 \uc11c\ube44\uc2a4\ub97c \uc704\ud55c \ub7a8\ub529\ud398\uc774\uc9c0

### \uae30\uc220 \uc2a4\ud0dd
- \uc21c\uc218 \uc815\uc801 \uc0ac\uc774\ud2b8 (HTML/CSS/JS)
- GitHub Pages \ud638\uc2a4\ud305
- PWA \uc9c0\uc6d0

### \ud575\uc2ec \uac00\uce58
- \ubaa8\ubc14\uc77c \ud37c\uc2a4\ud2b8
- \uc11c\ubc84 \uc5c6\uc774 \ub3c5\ub9bd \ub3d9\uc791
- \ubcc0\uc218\ud654\ub41c config\ub85c \uc27d\uac8c \ubcf5\uc81c \uac00\ub2a5

---

## 2. \ud3f4\ub354 \uad6c\uc870

```
dtslib-branch/
\u251c\u2500\u2500 index.html              # \uba54\uc778 \ub7a8\ub529\ud398\uc774\uc9c0
\u251c\u2500\u2500 config.json             # \uc911\uc559 \uc124\uc815 \ud30c\uc77c
\u251c\u2500\u2500 CNAME                   # \ucee4\uc2a4\ud140 \ub3c4\uba54\uc778 (dtslib.com)
\u251c\u2500\u2500 robots.txt              # SEO
\u251c\u2500\u2500 sitemap.xml             # \uc0ac\uc774\ud2b8\ub9f5
\u251c\u2500\u2500 sw.js                   # Service Worker (PWA)
\u251c\u2500\u2500 .nojekyll               # Jekyll \ube44\ud65c\uc131\ud654
\u2502
\u251c\u2500\u2500 assets/
\u2502   \u251c\u2500\u2500 manifest.json       # PWA \uc124\uc815
\u2502   \u2514\u2500\u2500 icons/
\u2502       \u2514\u2500\u2500 logo.png        # \uc571 \uc544\uc774\ucf58 (TODO: \ucd94\uac00 \ud544\uc694)
\u2502
\u2514\u2500\u2500 staff/
    \u2514\u2500\u2500 index.html          # \uc2a4\ud0dc\ud504 \ud3ec\ud138 (\ube44\ubc00\ubc88\ud638: 1126)
```

---

## 3. \uc124\uc815 \ud30c\uc77c (config.json)

\ubaa8\ub4e0 \ubcc0\uc218\ud654\ub41c \uac12\uc740 `config.json`\uc5d0 \uc9d1\uc911\ub418\uc5b4 \uc788\uc2b5\ub2c8\ub2e4.

### \uc8fc\uc694 \uc124\uc815
| \ud56d\ubaa9 | \ud604\uc7ac \uac12 | \uc124\uba85 |
|------|----------|------|
| `site.name` | dtslib \ucee8\uc124\ud305 | \uc0ac\uc774\ud2b8\uba85 |
| `site.domain` | dtslib.com | \ub3c4\uba54\uc778 |
| `owner.email` | dimas@dtslib.com | \uc5f0\ub77d\ucc98 |
| `service.price` | 25\ub9cc\uc6d0 / 2\uc2dc\uac04 | \uc11c\ube44\uc2a4 \uac00\uaca9 |
| `staff.accessCode` | 1126 | \uc2a4\ud0dc\ud504 \ud3ec\ud138 \ube44\ubc00\ubc88\ud638 |

### \ubcf5\uc81c \uc2dc \ubcc0\uacbd \ud56d\ubaa9
1. `config.json` \uc218\uc815
2. `CNAME` \ud30c\uc77c \uc218\uc815
3. `index.html` \ub0b4 \ud558\ub4dc\ucf54\ub529\ub41c \uac12 \uc218\uc815
4. `assets/manifest.json` \uc218\uc815

---

## 4. \ucee4\ubc0b \ucee8\ubca4\uc158

```
feat: \uc0c8 \uae30\ub2a5 \ucd94\uac00
fix: \ubc84\uadf8 \uc218\uc815
docs: \ubb38\uc11c \uc5c5\ub370\uc774\ud2b8
style: \ub514\uc790\uc778 \ubcc0\uacbd
refactor: \uad6c\uc870 \uac1c\uc120
```

---

## 5. \ubc30\ud3ec

### GitHub Pages \uc124\uc815
1. Settings \u2192 Pages
2. Source: `main` branch
3. Custom domain: `dtslib.com`

### DNS \uc124\uc815
CNAME \ub808\ucf54\ub4dc: `dtslib1979.github.io`

---

## 6. TODO

- [ ] \ub85c\uace0 \uc774\ubbf8\uc9c0 \ucd94\uac00 (`assets/icons/logo.png`)
- [ ] OG \uc774\ubbf8\uc9c0 \ucd94\uac00
- [ ] DNS \uc124\uc815 \uc644\ub8cc
- [ ] \ucd94\uac00 \ud398\uc774\uc9c0 \ud544\uc694 \uc2dc \ud655\uc7a5

---

## 7. \ubcf4\uc77c\ub7ec\ud50c\ub808\uc774\ud2b8 \uae30\ubc18

\uc774 \ud504\ub85c\uc81d\ud2b8\ub294 `buddies.kr` \ub808\ud3ec\uc9c0\ud1a0\ub9ac\ub97c \uae30\ubc18\uc73c\ub85c \ubcf5\uc81c/\ubcc0\ud615\ub418\uc5c8\uc2b5\ub2c8\ub2e4.

### \ubcc0\uacbd \uc0ac\ud56d
| buddies \uc6d0\ubcf8 | dtslib \ubcc0\uacbd |
|--------------|----------------|
| buddies.kr | dtslib.com |
| \ub85c\ucee8 \ud56b\ud50c\ub808\uc774\uc2a4 \uc2dc\uc2a4\ud15c | AI \uc5c5\ubb34 \uc790\ub3d9\ud654 \uc138\ud305 |
| pro@buddies.kr | dimas@dtslib.com |
| Daniel/Justin/Thomas | DIMAS |
| 18 Holes \uce90\ub7ec\uc140 | \uc81c\uac70 |
| Portfolio \uc139\uc158 | \uc81c\uac70 |

---

*\ub9c8\uc9c0\ub9c9 \uc5c5\ub370\uc774\ud2b8: 2026-01-12*
---

## Browser Runtime

> Parksy OS 2+2 매트릭스 — 이 레포 전담 브라우저

| 항목 | 값 |
|------|-----|
| **브라우저** | Google Chrome |
| **이유** | 프랜차이즈 OS 보일러플레이트 — 코드 시연 |
| **URL** | https://dtslib.com |


---

## ⚡ 전역 컨텍스트 — 반드시 읽어라 (2026-03-16 갱신)

> **세션 시작 시 이 블록을 먼저 읽는다. 모든 하위 조항보다 우선한다.**

### 패러다임 전환 (특별법 제0조)

| | Before | After (지금) |
|---|---|---|
| 메인 기기 | 핸드폰 (Termux) | 집 PC (WSL2) |
| 보조 기기 | PC (원격 서버) | 핸드폰 (SSH 클라이언트) |
| 브라우저 자동화 | headless 우회, ADB 체인 | PC Chrome 직접 (Playwright headless=False) |
| 배치 작업 | 핸드폰 한 세션 | tmux 던져놓고 퇴근 |

### 죽은 패턴 (절대 부활 금지)
```
❌ headless Chromium 우회
❌ ADB 체인
❌ 핸드폰에서 CDP 흉내
❌ 세션 1개 제약 설계
```

### 현재 작업 표준
```
핸드폰 → Tailscale SSH → 집 PC WSL2 → Claude Code
텔레그램 봇 → tmux 배치 세션 (tg-image, tg-audio)
브라우저 자동화 → Windows Chrome Playwright headless=False
```

### SCM 자동화 개발 시퀀스 (진행 중)
```
1. 텔레그램 봇        ✅ 완료 (2026-03-16)
2. 티스토리 자동화    🔄 진행 중 — Playwright headless=False
3. 네이버 자동화      ⏳ 대기 — login.cjs PC-native 교체
4. YouTube 자동화     ⏳ 대기 — Draft injection, OAuth 정상화
5. Google 자동화      ⏳ 대기
   ↓
6. APK 업데이트       ⏳ 대기
7. 워크센터 레포 정비 ⏳ 대기 (28개)
8. 양산               ⏳ 대기
```

### 지금 당장 막힌 것
- 티스토리 19개 블로그 스킨 삽입 미완료 (player.html)
- 티스토리 25슬롯 서브도메인 미확보
- 관련 스크립트: `C:\Temp\tistory_auto_v2.py`

---
