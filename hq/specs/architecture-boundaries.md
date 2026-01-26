# DTSLIB Franchise OS — Architecture Boundaries v1.0

> 4개 경계만 고정하면 시스템이 완성된다.

---

## Boundary 1: HQ vs Secret Office

```
┌─────────────────────────────────────────────────────────────┐
│                      HQ (Control Plane)                     │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │
│  │  Brief  │  │  Inbox  │  │ Release │  │  Registry   │    │
│  │ 방향/룰  │  │  수집함  │  │ 배포버튼 │  │ branches.json│    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────┘    │
│                                                             │
│  ❌ 제작 도구 금지 (HTMLPost 등은 Secret Office로)           │
└─────────────────────────────────────────────────────────────┘
                              │
                    방향 내려줌 / 결과물 수집
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Secret Office (Workbench)                    │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │
│  │  Brief  │  │ Create  │  │ Publish │  │ Tools Lab   │    │
│  │ HQ에서↓ │  │ 글/영상  │  │ 외부발행 │  │ Builder만   │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────┘    │
│                                                             │
│  ✅ 생산은 여기서만                                          │
└─────────────────────────────────────────────────────────────┘
```

### HQ 역할 (4개만)
| 메뉴 | 기능 |
|------|------|
| **Brief** | 이번 주/오늘 방향 3줄 |
| **Inbox** | 카톡/음성/링크 수집 (던지는 곳) |
| **Release** | 배포 버튼, 태그/버전 |
| **Registry** | branches.json 단일 진실 |

### Secret Office 역할 (3+1개)
| 메뉴 | 기능 | 권한 |
|------|------|------|
| **Brief** | HQ에서 내려온 방향 표시 | 전원 |
| **Create** | 글/영상/이미지 제작 | 전원 |
| **Publish** | YouTube/Tistory/GitHub 발행 | 전원 |
| **Tools Lab** | APK/PWA/SDK | Builder만 |

---

## Boundary 2: 배포 단위 = Chalkboard Pack

```
"앱 배포" 금지
"칠판 팩 배포"만 존재
```

### Chalkboard Pack 구성
```
/<branch>/chalkboard/
├── index.html      # 칠판 UI (필수)
├── board.json      # 오늘 데이터 (필수)
└── README.md       # 촬영 루틴 (필수)
```

### PWA/APK 위치
```
PWA = URL "설치" → 포장 옵션
APK = 오버레이 필요시 → 포장 옵션

기본은 항상 HTML
```

---

## Boundary 3: 단일 진실 = branches.json

```json
{
  "branches": [{
    "id": "koosy",
    "governance": "collaborator",
    "cognitive": "hybrid",
    "hqAccess": ["templates", "sync", "claude-code", "broadcast"]
  }]
}
```

### UI 노출 규칙 (10줄)

```javascript
// branches.json → UI 노출 결정
const rules = {
  // broadcast 있으면
  "broadcast": ["REC", "칠판", "스튜디오"],

  // claude-code 있으면
  "claude-code": ["오빗 프롬프트", "템플릿 편집"],

  // sdk 있으면
  "sdk": ["PWA 래핑", "APK 빌드", "Tools Lab"]
};

function getVisibleMenus(branch) {
  return branch.hqAccess.flatMap(access => rules[access] || []);
}
```

### 권한 원칙
```
권한 = "막는 것"이 아니라 "보이는 것"을 조절
전원 업로드 가능, 차이는 "뭘 보여주냐"
```

---

## Boundary 4: 파이프라인 = Orbit → Generate → Release

```
┌─────────────────────────────────────────────────────────┐
│                    Daily Pipeline                       │
│                                                         │
│  1. HQ Brief 작성 (3줄)                                  │
│           ↓                                             │
│  2. Inbox 수집 (카톡/음성/링크)                           │
│           ↓                                             │
│  3. Orbit Prompt + 변수 → index.html 생성               │
│           ↓                                             │
│  4. HQ Release → /<branch>/chalkboard/ 배포             │
│           ↓                                             │
│  5. Branch Secret Office → REC → 촬영                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 역할 분리
```
제작자: "코드" 몰라도 됨 → REC만 누르면 됨
HQ: "생성/배포"만 책임
```

---

## 아키텍처 요약

| 영역 | 정체 | 담당 |
|------|------|------|
| **HQ** | Control Plane | Registry / Brief / Inbox / Release |
| **Secret Office** | Workbench | Create / Upload / Publish (+ Builder Lab) |
| **Artifact** | Chalkboard Pack | index.html + board.json + README |
| **Rule Source** | branches.json | 메뉴 노출 / 권한 / 배포 타깃 전부 결정 |

---

## CLI 명령어 (예정)

```bash
# HQ 운영
dts brief <branch_id>      # Brief 전송
dts inbox list             # 수집함 확인
dts release <branch_id>    # 칠판 팩 배포
dts release --all          # 전체 배포

# Branch 운영
dts pull                   # 최신 칠판 팩 가져오기
dts status                 # 현재 상태 확인
```

---

*Version: 1.0*
*Created: 2026-01-26*
*Authority: DTSLIB HQ*
