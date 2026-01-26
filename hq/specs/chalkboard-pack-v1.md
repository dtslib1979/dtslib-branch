# Chalkboard Pack v1 Specification

> 배포 단위의 단일 표준. "앱 배포" 금지 — "칠판 팩 배포"만 존재한다.

---

## 1. 폴더 구조

```
/<branch>/chalkboard/
├── index.html      # 칠판 UI (필수)
├── board.json      # 오늘 카드/주제 데이터 (필수)
└── README.md       # 촬영 루틴 10줄 (필수)
```

### 경로 규칙
- 모든 브랜치는 루트에 `/chalkboard/` 폴더 보유
- HQ에서 배포 시 이 폴더만 덮어쓰기
- PWA/APK는 이 폴더를 래핑할 뿐, 구조 변경 금지

---

## 2. index.html 필수 UI 체크리스트

### 2.1 문서 구조
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{BRANCH_NAME} Chalkboard</title>
  <!-- 외부 라이브러리 금지: 순수 HTML/CSS/JS만 -->
</head>
```

### 2.2 필수 섹션 (순서 고정)

| 순서 | 섹션 | ID | 설명 |
|------|------|----|------|
| 1 | Header | `#header` | Day X / 제목 / 브랜치명 |
| 2 | Chalkboard | `#chalkboard` | 카드 3~6개 그리드 |
| 3 | Topic | `#topic` | 오늘의 주제 (1줄) |
| 4 | REC | `#btn-rec` | 촬영 시작 버튼 (가장 큼) |
| 5 | Quick Access | `#quick-access` | Archive / Engine / GitHub / Guide |

### 2.3 필수 요소 ID

```html
<!-- Header -->
<header id="header">
  <span id="day-count">Day 1</span>
  <h1 id="board-title">Today's Board</h1>
  <span id="branch-name">KOOSY</span>
</header>

<!-- Chalkboard Cards -->
<section id="chalkboard">
  <div class="card" data-link="...">...</div>
  <!-- 3~6개 -->
</section>

<!-- Today's Topic -->
<section id="topic">
  <p id="topic-text">오늘의 주제</p>
</section>

<!-- REC Button -->
<button id="btn-rec">● REC</button>

<!-- Quick Access -->
<nav id="quick-access">
  <a id="link-archive" href="...">Archive</a>
  <a id="link-engine" href="...">Engine</a>
  <a id="link-github" href="...">GitHub</a>
  <a id="link-guide" href="...">Guide</a>
</nav>
```

### 2.4 스타일 규칙

```css
/* 필수 규격 */
body {
  max-width: 420px;      /* 모바일 1열 */
  margin: 0 auto;
  background: #0a0a0a;   /* 어두운 테마 */
  color: #ffffff;
}

#btn-rec {
  /* 강조색 1개만 사용 */
  background: var(--accent);
  /* 최소 높이 */
  min-height: 64px;
}
```

### 2.5 JS 필수 동작

```javascript
// 1. 카드 클릭 → 링크 열기
document.querySelectorAll('.card').forEach(card => {
  card.onclick = () => window.open(card.dataset.link);
});

// 2. REC 클릭 → #chalkboard로 스크롤
document.getElementById('btn-rec').onclick = () => {
  document.getElementById('chalkboard').scrollIntoView();
};

// 3. board.json 로드 (있으면)
fetch('board.json')
  .then(r => r.json())
  .then(data => renderBoard(data))
  .catch(() => console.log('Static mode'));
```

---

## 3. board.json 스키마

```json
{
  "$schema": "chalkboard-pack-v1",
  "version": "1.0",
  "branch": {
    "id": "koosy",
    "name": "KOOSY",
    "accent": "#ff6b35"
  },
  "board": {
    "day": 1,
    "title": "Today's Chalkboard",
    "date": "2026-01-26"
  },
  "topic": "오늘의 주제를 한 줄로",
  "cards": [
    {
      "icon": "📺",
      "title": "Card Title",
      "subtitle": "설명 텍스트",
      "link": "https://..."
    }
  ],
  "quickAccess": {
    "archive": "https://...",
    "engine": "https://...",
    "github": "https://...",
    "guide": "https://..."
  }
}
```

### 필드 규칙

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `branch.id` | string | ✅ | branches.json의 id와 일치 |
| `branch.name` | string | ✅ | 표시명 |
| `branch.accent` | hex color | ✅ | 강조색 1개 |
| `board.day` | number | ✅ | 방송 일차 |
| `board.title` | string | ✅ | 칠판 제목 |
| `board.date` | ISO date | ✅ | 발행일 |
| `topic` | string | ✅ | 오늘의 주제 (1줄) |
| `cards` | array | ✅ | 3~6개 |
| `cards[].icon` | emoji | ✅ | 이모지 1개 |
| `cards[].title` | string | ✅ | 카드 제목 |
| `cards[].subtitle` | string | ❌ | 부제 |
| `cards[].link` | URL | ✅ | 클릭 시 이동 |
| `quickAccess` | object | ✅ | 하단 링크 4개 |

---

## 4. Release 규칙

### 4.1 배포 명령 (HQ → Branch)

```bash
# 단일 브랜치 배포
dts release <branch_id>

# 전체 브랜치 배포
dts release --all
```

### 4.2 배포 체크리스트

```
□ board.json 스키마 검증 통과
□ index.html 필수 ID 존재 확인
□ 카드 개수 3~6개 범위
□ accent 색상 유효한 hex
□ 모든 link URL 유효
```

### 4.3 버전 태깅

```
chalkboard-{branch_id}-{YYYYMMDD}-{seq}

예: chalkboard-koosy-20260126-01
```

### 4.4 배포 후 자동 실행

1. `/<branch>/chalkboard/` 덮어쓰기
2. Git commit with tag
3. (broadcast 권한 있으면) 브랜치에 알림

---

## 5. PWA/APK 래핑 (옵션)

> Builder(sdk 권한 보유자)만 해당

### PWA
- `manifest.json`에 `start_url: "/chalkboard/"` 지정
- Service Worker는 chalkboard 폴더만 캐싱

### APK
- WebView로 `index.html` 로드
- 오버레이 권한 필요 시에만 APK 선택
- 기본은 PWA 권장

---

## 6. Orbit Prompt 연동

Chalkboard Pack 생성 시 사용하는 프롬프트 변수:

```
{BRANCH_ID}      → branch.id
{BRANCH_NAME}    → branch.name
{ACCENT_COLOR}   → branch.accent
{DAY_COUNT}      → board.day
{BOARD_TITLE}    → board.title
{TOPIC}          → topic
{CARDS_JSON}     → cards 배열
{QUICK_ACCESS}   → quickAccess 객체
```

---

*Version: 1.0*
*Created: 2026-01-26*
*Authority: DTSLIB HQ*
