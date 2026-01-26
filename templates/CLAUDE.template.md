# {REPO_NAME} — Agent Protocol v1.0

> {TAGLINE}

---

## 1. Identity

| 항목 | 값 |
|------|-----|
| **Tier** | {TIER_LEVEL} |
| **Parent** | {PARENT_HQ} |
| **Type** | {REPO_TYPE} |
| **Domain** | {DOMAIN_URL} |

### Purpose
{PURPOSE_DESCRIPTION}

### Tech Stack
- 순수 정적 사이트 (HTML/CSS/JS)
- GitHub Pages 호스팅
- DTSLIB Design System

---

## 2. Hierarchy

```
dtslib-papyrus (Tier 1)
    │
    ├── dtslib-branch (Tier 2)
    │
    └── espiritu-tango (Tier 2 - Studio HQ)
            │
            └── {REPO_NAME} (Tier 3) ← 현재 위치
```

---

## 3. Core Files

| 파일 | 용도 |
|------|------|
| `index.html` | 메인 랜딩 |
| `CLAUDE.md` | 에이전트 프로토콜 (이 파일) |
| `FACTORY.json` | 설정 메타데이터 |
| `branch.json` | HQ 연동 정보 |
| `design/` | 디자인 시스템 |

---

## 4. Commit Convention

```
feat: 새 기능
fix: 버그 수정
content: 콘텐츠 추가/수정
design: 디자인 변경
docs: 문서 변경
```

커밋 메시지 끝에 항상 추가:
```
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## 5. Forbidden Terms

사용 금지 (해당 시):
{FORBIDDEN_TERMS}

---

## 6. LLM Control Interface

이 레포는 GitHub 폐쇄 생태계 내에서 LLM으로 제어됨.

| Action | Method |
|--------|--------|
| READ | `git clone` / file read |
| WRITE | file write / `git commit` |
| EXECUTE | GitHub Actions |
| STATE | `git log` / file content |

---

*Last updated: {DATE}*
*Version: 1.0*
*Affiliation: DTSLIB HQ*
