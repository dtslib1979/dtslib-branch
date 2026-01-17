# {{PROJECT_NAME}} 에이전트 프로토콜

> 이 문서는 Claude Code가 {{PROJECT_NAME}} 레포지토리에서 작업할 때 따라야 하는 가이드입니다.

---

## 1. 프로젝트 개요

### 목적
{{PROJECT_DESCRIPTION}}

### 기술 스택
- 순수 정적 사이트 (HTML/CSS/JS)
- GitHub Pages 호스팅

### 소속
- **본사**: dtslib-branch (HQ)
- **레포**: {{REPO_NAME}}
- **도메인**: {{DOMAIN}}

---

## 2. 폴더 구조

```
{{PROJECT_ID}}/
├── index.html              # 메인 페이지
├── config.json             # 설정 파일
├── CLAUDE.md               # 이 문서
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── pages/                  # 추가 페이지
```

---

## 3. 커밋 컨벤션

```
feat: 새 기능 추가
fix: 버그 수정
docs: 문서 업데이트
style: 디자인 변경
refactor: 구조 개선
```

---

## 4. 작업 시 주의사항

1. 수정 전 반드시 `git pull` 실행
2. 커밋 메시지는 한글로 명확하게
3. 큰 변경은 브랜치 생성 후 PR
4. 민감 정보 커밋 금지

---

## 5. HQ 연동

이 프로젝트는 DTSLIB HQ (dtslib-branch)에서 관리됩니다.

- HQ 레포: `dtslib1979/dtslib-branch`
- 브랜치 설정: `hq/branches.json`

---

*마지막 업데이트: {{DATE}}*
