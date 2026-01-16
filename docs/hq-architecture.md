# DTSLIB HQ 아키텍처 설계

> dtslib-branch를 본사(HQ)로 하여 koosy, gohsy, papafly 브랜치를 통합 관리하는 시스템 아키텍처

---

## 1. 시스템 개요

### 비전
```
┌─────────────────────────────────────────────────────────────────┐
│                        DTSLIB HQ (본사)                          │
│                      dtslib-branch repo                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Private LLM Engine                    │    │
│  │            (미래: 나만의 LLM / Claude API)               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                    ┌─────────┴─────────┐                        │
│                    │   Request Router   │                        │
│                    │   (요청 분배기)     │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │   KOOSY     │     │   GOHSY     │     │  PAPAFLY    │
    │  (셀럽방송)  │     │  (소원실현)  │     │ (인큐베이션) │
    │   public    │     │   private   │     │   private   │
    └─────────────┘     └─────────────┘     └─────────────┘
```

### 핵심 목표
1. **중앙 집중 관리**: HQ에서 모든 브랜치 프로젝트 통제
2. **LLM 자동화**: 카카오톡 요청 → LLM 처리 → 코드 자동 생성/수정
3. **확장 가능성**: 새로운 브랜치 프로젝트 쉽게 추가

---

## 2. 브랜치 프로젝트 정의

### 2.1 KOOSY (koosy repo)
| 항목 | 내용 |
|------|------|
| **도메인** | koosy.dtslib.com (예정) |
| **성격** | 셀럽 스토리 편집 방송 |
| **공개** | Public |
| **주요 기능** | 블러핑 기반 편집, 스토리텔링 |

### 2.2 GOHSY (gohsy repo)
| 항목 | 내용 |
|------|------|
| **도메인** | gohsy.dtslib.com (예정) |
| **성격** | 소원 실현 플랫폼 |
| **공개** | Private |
| **주요 기능** | 목표 설정, 달성 추적 |

### 2.3 PAPAFLY (papafly repo)
| 항목 | 내용 |
|------|------|
| **도메인** | papafly.dtslib.com (예정) |
| **성격** | 인큐베이션 프로젝트 |
| **공개** | Private |
| **주요 기능** | 실험적 기능, 프로토타입 |

---

## 3. HQ 시스템 구성요소

### 3.1 디렉토리 구조 (확장 계획)
```
dtslib-branch/
├── index.html              # HQ 대시보드
├── config.json             # 중앙 설정
├── CLAUDE.md               # AI 에이전트 가이드
│
├── hq/                     # 🆕 본사 시스템
│   ├── router.js           # 요청 라우터
│   ├── branches.json       # 브랜치 레지스트리
│   └── llm-config.json     # LLM 설정
│
├── api/                    # 🆕 API 엔드포인트 (Cloudflare Workers)
│   ├── kakao-webhook.js    # 카카오톡 웹훅 수신
│   ├── llm-proxy.js        # LLM API 프록시
│   └── github-dispatch.js  # GitHub Actions 트리거
│
├── docs/
│   ├── hq-architecture.md  # 이 문서
│   └── api-spec.md         # API 명세
│
└── tools/                  # 자동화 도구
    ├── branch-sync.sh      # 브랜치 동기화
    └── deploy-all.sh       # 전체 배포
```

### 3.2 브랜치 레지스트리 (branches.json)
```json
{
  "branches": [
    {
      "id": "koosy",
      "repo": "dtslib1979/koosy",
      "domain": "koosy.dtslib.com",
      "status": "active",
      "features": ["story-edit", "celeb-content"],
      "kakaoChannel": "@koosy"
    },
    {
      "id": "gohsy",
      "repo": "dtslib1979/gohsy",
      "domain": "gohsy.dtslib.com",
      "status": "active",
      "features": ["wish-tracking", "goal-setting"],
      "kakaoChannel": "@gohsy"
    },
    {
      "id": "papafly",
      "repo": "dtslib1979/papafly",
      "domain": "papafly.dtslib.com",
      "status": "incubation",
      "features": ["experimental"],
      "kakaoChannel": "@papafly"
    }
  ],
  "hq": {
    "repo": "dtslib1979/dtslib-branch",
    "domain": "dtslib.com",
    "adminChannel": "@dtslib"
  }
}
```

---

## 4. 카카오톡 → LLM → 코드 파이프라인

### 4.1 요청 흐름
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   카카오톡    │───▶│  Cloudflare  │───▶│   DTSLIB     │
│   사용자      │    │   Workers    │    │   Private    │
│   @koosy     │    │  (Webhook)   │    │     LLM      │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                                               ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   GitHub     │◀───│   코드 생성   │◀───│   의도 분석   │
│   Actions    │    │   /수정      │    │   태스크화   │
│   (Deploy)   │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  자동 배포    │───▶│   결과 알림   │───▶ 카카오톡 응답
│  (각 브랜치)  │    │   (완료/에러) │
└──────────────┘    └──────────────┘
```

### 4.2 요청 예시
```
사용자 (카카오톡 @koosy):
"메인 페이지에 새 셀럽 카드 추가해줘.
 이름: 김태희, 이미지: taehee.jpg"

LLM 처리:
1. 의도 파악: koosy 레포 > index.html > 셀럽 카드 추가
2. 코드 생성: HTML 카드 컴포넌트
3. PR 생성 또는 직접 커밋
4. GitHub Actions 트리거
5. 배포 완료 후 카카오톡 응답
```

### 4.3 명령어 체계
| 명령어 | 설명 | 대상 |
|--------|------|------|
| `/add [내용]` | 콘텐츠 추가 | 해당 브랜치 |
| `/edit [대상] [내용]` | 기존 콘텐츠 수정 | 해당 브랜치 |
| `/deploy` | 수동 배포 트리거 | 해당 브랜치 |
| `/status` | 현재 상태 확인 | HQ |
| `/sync` | 브랜치 동기화 | HQ |

---

## 5. LLM 통합 계획

### 5.1 Phase 1: Claude API 연동 (현재 가능)
```
Cloudflare Workers
       │
       ▼
  Claude API (Anthropic)
       │
       ▼
  GitHub API (코드 수정)
```

**장점**: 즉시 구현 가능, 높은 성능
**비용**: API 호출당 과금

### 5.2 Phase 2: Self-hosted LLM (미래)
```
Cloudflare Workers
       │
       ▼
  Private LLM Server
  (Llama / Mistral / Custom)
       │
       ▼
  GitHub API
```

**장점**: 완전한 통제, 무제한 사용
**요구사항**: GPU 서버, 모델 파인튜닝

### 5.3 LLM 설정 파일 (llm-config.json)
```json
{
  "provider": "claude",
  "model": "claude-3-opus",
  "fallback": "claude-3-sonnet",
  "systemPrompt": "DTSLIB HQ 자동화 에이전트...",
  "branchContexts": {
    "koosy": "셀럽 콘텐츠 편집 전문가",
    "gohsy": "목표 달성 코칭 전문가",
    "papafly": "실험적 기능 프로토타이퍼"
  },
  "permissions": {
    "autoCommit": false,
    "autoDeploy": false,
    "requireApproval": true
  }
}
```

---

## 6. 보안 설계

### 6.1 인증 레이어
```
카카오톡 사용자
       │
       ▼
┌─────────────────┐
│  인증 레이어     │
│  - 허용된 사용자 │
│  - 채널별 권한   │
└─────────────────┘
       │
       ▼
  LLM 처리
```

### 6.2 권한 매트릭스
| 역할 | koosy | gohsy | papafly | HQ |
|------|-------|-------|---------|-----|
| Admin | RWD | RWD | RWD | RWD |
| Editor | RW | RW | R | R |
| Viewer | R | R | R | R |

R=Read, W=Write, D=Deploy

### 6.3 시크릿 관리
- GitHub Secrets: API 키, 토큰
- Cloudflare Workers Secrets: 환경변수
- 로컬 저장 금지: 모든 시크릿은 클라우드에만

---

## 7. 구현 로드맵

### Phase 1: 기반 구축 (1주차)
- [ ] branches.json 생성 및 레지스트리 구축
- [ ] hq/ 디렉토리 구조 생성
- [ ] 기본 라우터 로직 설계

### Phase 2: 카카오톡 연동 (2주차)
- [ ] Cloudflare Workers 설정
- [ ] 카카오톡 채널 웹훅 연결
- [ ] 메시지 파싱 로직

### Phase 3: LLM 파이프라인 (3주차)
- [ ] Claude API 연동
- [ ] 의도 분석 프롬프트 설계
- [ ] 코드 생성 템플릿

### Phase 4: GitHub 자동화 (4주차)
- [ ] GitHub Actions 워크플로우
- [ ] 자동 PR 생성
- [ ] 배포 파이프라인

### Phase 5: 고도화 (지속)
- [ ] Private LLM 검토
- [ ] 모니터링 대시보드
- [ ] 에러 핸들링 강화

---

## 8. 기술 스택 요약

| 영역 | 기술 |
|------|------|
| **HQ 프론트** | HTML/CSS/JS (정적) |
| **API 레이어** | Cloudflare Workers |
| **LLM** | Claude API → Private LLM |
| **버전관리** | GitHub |
| **CI/CD** | GitHub Actions |
| **메시징** | 카카오톡 채널 API |
| **호스팅** | GitHub Pages / Cloudflare Pages |

---

## 9. 참고 다이어그램

### 전체 시스템 흐름
```
┌─────────────────────────────────────────────────────────────────────────┐
│                              DTSLIB ECOSYSTEM                            │
│                                                                         │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │ 카카오톡 │────▶│ CF      │────▶│   LLM   │────▶│ GitHub  │          │
│  │ 요청    │     │ Workers │     │ Engine  │     │ API     │          │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │
│                                                        │               │
│                        ┌───────────────────────────────┘               │
│                        │                                               │
│                        ▼                                               │
│  ┌─────────────────────────────────────────────────────────┐          │
│  │                    dtslib-branch (HQ)                    │          │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │          │
│  │  │ Router  │  │ Config  │  │ Monitor │  │ Deploy  │    │          │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │          │
│  └─────────────────────────────────────────────────────────┘          │
│                        │                                               │
│          ┌─────────────┼─────────────┐                                │
│          │             │             │                                │
│          ▼             ▼             ▼                                │
│     ┌─────────┐   ┌─────────┐   ┌─────────┐                          │
│     │  KOOSY  │   │  GOHSY  │   │ PAPAFLY │                          │
│     │ 셀럽방송 │   │ 소원실현 │   │인큐베이션│                          │
│     └─────────┘   └─────────┘   └─────────┘                          │
│          │             │             │                                │
│          ▼             ▼             ▼                                │
│     [배포완료]    [배포완료]    [배포완료]                             │
│          │             │             │                                │
│          └─────────────┼─────────────┘                                │
│                        │                                               │
│                        ▼                                               │
│                 ┌─────────────┐                                        │
│                 │ 카카오톡 응답 │                                        │
│                 │ "완료!"      │                                        │
│                 └─────────────┘                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*작성일: 2026-01-16*
*버전: 1.0*
*작성: DTSLIB HQ / Claude Code*
