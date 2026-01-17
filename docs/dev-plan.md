# DTSLIB HQ 개발 계획서

> koosy, gohsy, papafly 브랜치를 통합 관리하는 본사 시스템 개발 계획

---

## 1. 프로젝트 개요

### 목표
dtslib-branch를 본사(HQ)로 하여 3개 브랜치 프로젝트를 중앙에서 관리하고, 카카오톡 요청을 Claude Code가 처리하여 자동으로 코드를 생성/수정/배포하는 시스템 구축

### 관리 대상 레포지토리
| 레포 | 용도 | 공개 |
|------|------|------|
| dtslib-branch | HQ (본사) | public |
| koosy | 셀럽 스토리 방송 | public |
| gohsy | 소원 실현 플랫폼 | private |
| papafly | 인큐베이션 | private |

### 기술 스택 (단순화)
```
Termux + Claude Code + GitHub (Actions/Pages)
```
- **별도 서버 없음** (Cloudflare Workers 불필요)
- **비용: 무료**

---

## 2. 시스템 구조

### 운영 흐름
```
┌─────────────────────────────────────────────────────┐
│                    작업 흐름                         │
│                                                     │
│  1. 카카오톡으로 요청 수신                            │
│         │                                           │
│         ▼                                           │
│  2. Termux에서 Claude Code 실행                     │
│     $ claude                                        │
│         │                                           │
│         ▼                                           │
│  3. Claude가 해당 레포 clone/pull                   │
│     $ gh repo clone dtslib1979/koosy               │
│         │                                           │
│         ▼                                           │
│  4. 코드 수정 및 커밋                                │
│     $ git add . && git commit && git push          │
│         │                                           │
│         ▼                                           │
│  5. GitHub Actions 자동 배포                        │
│         │                                           │
│         ▼                                           │
│  6. 카카오톡으로 완료 알림                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 3. 개발 태스크

### Phase 1: HQ 기반 구축
**목표**: dtslib-branch에 브랜치 관리 체계 구축

| # | 태스크 | 파일/위치 | 상태 |
|---|--------|----------|------|
| 1.1 | 브랜치 레지스트리 생성 | `hq/branches.json` | 예정 |
| 1.2 | HQ 설정 파일 생성 | `hq/config.json` | 예정 |
| 1.3 | 브랜치별 CLAUDE.md 템플릿 | `hq/templates/` | 예정 |
| 1.4 | 빠른 이동 스크립트 | `tools/goto.sh` | 예정 |

### Phase 2: 각 브랜치 표준화
**목표**: koosy, gohsy, papafly에 통일된 구조 적용

| # | 태스크 | 대상 | 상태 |
|---|--------|------|------|
| 2.1 | CLAUDE.md 배포 | 3개 레포 | 예정 |
| 2.2 | config.json 표준화 | 3개 레포 | 예정 |
| 2.3 | GitHub Actions 워크플로우 | 3개 레포 | 예정 |
| 2.4 | 서브도메인 설정 | CNAME 파일 | 예정 |

### Phase 3: 자동화 도구
**목표**: 반복 작업 자동화 스크립트

| # | 태스크 | 설명 | 상태 |
|---|--------|------|------|
| 3.1 | 전체 동기화 스크립트 | 모든 레포 pull | 예정 |
| 3.2 | 전체 상태 확인 | git status 일괄 | 예정 |
| 3.3 | 빠른 배포 스크립트 | 선택 레포 push | 예정 |

### Phase 4: LLM 컨텍스트 최적화
**목표**: Claude Code가 각 프로젝트 맥락을 빠르게 파악

| # | 태스크 | 설명 | 상태 |
|---|--------|------|------|
| 4.1 | 프로젝트별 프롬프트 가이드 | 역할 정의 | 예정 |
| 4.2 | 코드 컨벤션 문서 | 스타일 통일 | 예정 |
| 4.3 | 자주 쓰는 명령어 모음 | 빠른 참조 | 예정 |

---

## 4. 파일 구조 계획

### dtslib-branch (HQ) 확장
```
dtslib-branch/
├── CLAUDE.md                 # HQ 에이전트 가이드
├── config.json               # HQ 설정
├── index.html                # HQ 대시보드
│
├── hq/                       # 🆕 본사 관리 시스템
│   ├── branches.json         # 브랜치 레지스트리
│   ├── config.json           # HQ 전역 설정
│   └── templates/            # 브랜치용 템플릿
│       ├── CLAUDE.template.md
│       ├── config.template.json
│       └── workflow.template.yml
│
├── tools/                    # 🆕 자동화 스크립트
│   ├── sync-all.sh           # 전체 레포 동기화
│   ├── status-all.sh         # 전체 상태 확인
│   ├── goto.sh               # 빠른 레포 이동
│   └── deploy.sh             # 배포 스크립트
│
└── docs/
    ├── hq-architecture.md    # 아키텍처 (완료)
    ├── dev-plan.md           # 이 문서
    └── commands.md           # 명령어 레퍼런스
```

---

## 5. branches.json 설계

```json
{
  "version": "1.0",
  "hq": {
    "repo": "dtslib1979/dtslib-branch",
    "localPath": "~/dtslib-branch",
    "domain": "dtslib.com"
  },
  "branches": [
    {
      "id": "koosy",
      "name": "KOOSY",
      "repo": "dtslib1979/koosy",
      "localPath": "~/koosy",
      "domain": "koosy.kr",
      "description": "셀럽 스토리 편집 방송",
      "status": "active",
      "public": true
    },
    {
      "id": "gohsy",
      "name": "GOHSY",
      "repo": "dtslib1979/gohsy",
      "localPath": "~/gohsy",
      "domain": "gohsy.kr",
      "description": "소원 실현 플랫폼",
      "status": "active",
      "public": false
    },
    {
      "id": "papafly",
      "name": "PAPAFLY",
      "repo": "dtslib1979/papafly",
      "localPath": "~/papafly",
      "domain": "papafly.kr",
      "description": "인큐베이션 프로젝트",
      "status": "incubation",
      "public": false
    }
  ]
}
```

---

## 6. 핵심 스크립트

### 6.1 goto.sh - 빠른 레포 이동
```bash
#!/bin/bash
# 사용법: source ~/dtslib-branch/tools/goto.sh koosy

case $1 in
  hq|branch)  cd ~/dtslib-branch ;;
  koosy)      cd ~/koosy ;;
  gohsy)      cd ~/gohsy ;;
  papafly)    cd ~/papafly ;;
  *)          echo "사용법: goto [hq|koosy|gohsy|papafly]" ;;
esac
```

### 6.2 sync-all.sh - 전체 동기화
```bash
#!/bin/bash
# 모든 브랜치 레포 최신화

repos=("dtslib-branch" "koosy" "gohsy" "papafly")

for repo in "${repos[@]}"; do
  echo "=== $repo 동기화 ==="
  cd ~/$repo 2>/dev/null && git pull || echo "$repo: 레포 없음"
done
```

### 6.3 status-all.sh - 전체 상태
```bash
#!/bin/bash
# 모든 브랜치 상태 확인

repos=("dtslib-branch" "koosy" "gohsy" "papafly")

for repo in "${repos[@]}"; do
  echo "=== $repo ==="
  cd ~/$repo 2>/dev/null && git status -s || echo "레포 없음"
done
```

---

## 7. Claude Code 작업 흐름

### 카카오톡 요청 처리 예시

**요청**: "koosy 메인페이지에 새 셀럽 추가해줘"

**Claude 작업 순서**:
```
1. cd ~/koosy && git pull
2. 파일 구조 파악 (ls, cat)
3. 수정 대상 파일 확인
4. 코드 수정 (Edit 도구)
5. git add && git commit && git push
6. "완료!" 응답
```

### 멀티 레포 작업 예시

**요청**: "모든 프로젝트 푸터에 2026 저작권 표시 추가"

**Claude 작업 순서**:
```
1. ~/koosy 수정 → commit → push
2. ~/gohsy 수정 → commit → push
3. ~/papafly 수정 → commit → push
4. 결과 요약 응답
```

---

## 8. 우선순위 및 일정

### 즉시 실행 (오늘)
- [x] 아키텍처 문서 작성 (완료)
- [x] 개발 계획서 작성 (이 문서)
- [ ] hq/ 디렉토리 생성
- [ ] branches.json 생성

### 단기 (이번 주)
- [ ] 자동화 스크립트 3종 작성
- [ ] 각 브랜치 레포 clone 및 동기화
- [ ] CLAUDE.md 템플릿 배포

### 중기 (2주 내)
- [ ] GitHub Actions 워크플로우 설정
- [ ] 서브도메인 연결

### 장기 (1개월)
- [ ] Private LLM 검토
- [ ] 대시보드 UI 개발

---

## 9. 성공 기준

| 항목 | 기준 |
|------|------|
| 레포 관리 | 4개 레포 동시 관리 가능 |
| 응답 속도 | 카톡 요청 → 배포 완료 5분 이내 |
| 자동화율 | 반복 작업 80% 스크립트화 |
| 문서화 | 모든 프로젝트 CLAUDE.md 보유 |

---

## 10. 다음 액션

1. **hq/ 디렉토리 생성** - 본사 시스템 기반
2. **branches.json 작성** - 브랜치 레지스트리
3. **스크립트 3종 작성** - sync, status, goto
4. **각 브랜치 레포 준비** - clone 및 구조 확인

---

*작성일: 2026-01-17*
*버전: 1.0*
*작성: DTSLIB HQ / Claude Code*
