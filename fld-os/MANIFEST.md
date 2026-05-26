# FLD OS — Manifest

## 구조

```
fld-os/
├── core/                    # FLD 코어 엔진
│   ├── ledger.py            # 항목 모델 + 장부 CRUD + 상태 머신 + 점수 평가
│   └── mcp_tools.py         # 10개 MCP 도구 인터페이스
├── mcp/
│   └── fld_mcp_sse.py       # MCP SSE 서버 (port 8090)
├── dashboard/
│   ├── index.html           # 웹 대시보드 (다크 테마)
│   └── api/stats.py         # Stats API (port 8091)
├── integration/             # 외부 시스템 연결 계층
│   ├── hq_sync.py           # HQ 장부 양방향 동기화
│   ├── phone_mcp_bridge.py  # 폰 MCP Distributor SSH 브릿지
│   └── parksy_watcher.py    # Parksy 로그 자동 감시 → Seed 등록
├── widgets/                 # Termux:Widget 7팩
│   ├── 01_capture.sh        # 로그 수집 → Seed
│   ├── 02_scenario.sh       # Seed 목록 조회
│   ├── 03_ledger_post.sh    # 새 Seed 직접 등록
│   ├── 04_filter.sh         # 계정/상태 필터링
│   ├── 05_pilot_launch.sh   # Candidate→Pilot 실행
│   ├── 06_logback.sh        # 변경 이력 조회
│   └── 07_protocol_pack.sh  # Protocol 자산 패키징
├── data/
│   └── ledger.jsonl         # FLD 장부 (append-only)
├── docs/                    # 문서
├── tests/                   # 테스트
├── scripts/                 # 보조 스크립트
└── fld                      # CLI 진입점
```

## 레이어 ↔ 레포 매핑

| FLD 레이어 | 레포 | 역할 |
|-----------|------|------|
| Capture Layer | parksy-logs | 로그 파일 수집 (Parksy Capture) |
| Voice Layer | parksy-audio | MCP voice:8015, TTS, GPT-SoVITS |
| Image Layer | parksy-image | 이미지 생성, FLUX/SD |
| Distribution Layer | telegram-bridges | 텔레그램/디스코드/유튜브 배포 |
| Core Engine | dtslib-branch/fld-os | FLD OS 코어 (이곳) |
| Knowledge Layer | OrbitPrompt | 프롬프트 관리, 지식베이스 |
| Infrastructure | dtslib-localpc | 로컬 PC 실행 환경 |
| HQ Backbone | dtslib-branch/hq | 본사 트랜잭션 장부 |

## 상태 모델

```
🌱 Seed ──→ 📋 Scenario ──→ 🔍 Candidate ──→ 🧪 Pilot ──→ 📦 Protocol
  (입력)      (장면화)        (평가)           (실행)        (자산화)
```

### 전이 조건

| 전이 | 조건 |
|------|------|
| Seed → Scenario | raw_source 필수 |
| Scenario → Candidate | account (계정군) 분류 필수 |
| Candidate → Pilot | score ≥ 30 (50점 만점) |
| Pilot → Protocol | links (자산 URI) 필수 |

## 점수 체계 (10항목 × 5점 = 50점)

| 항목 | 설명 |
|------|------|
| immediacy | 당장 실행 가능성 |
| mobile_fit | 모바일 적합성 |
| log_value | 장기 자산 가치 |
| reusability | 재사용성 |
| deployability | 배포 가능성 (GitHub/Pages/APK/PWA) |
| mcp_potential | 도구/규칙 승격 가능성 |
| revenue_potential | 수익 직간접 기여 |
| brand_fit | Phone-first/박씨 세계관 부합 |
| maintainability | 유지보수 비용 적정성 |
| evidence | Pilot 결과 회수 가능성 |

## 계정군 (8종)

person, space, revenue, channel, content, tool, risk, asset

## CLI

```
fld seed <title> [motive] [account]   — 새 Seed
fld list [state]                       — 목록
fld state <id> <to> [by]              — 상태 전이
fld score <id>                         — 점수 평가
fld stats                              — 통계
fld ingest                             — 로그→Seed 자동
fld watch [interval]                   — 로그 실시간 감시
fld hq-sync                            — HQ 동기화
fld phone [status|call|distribute]     — 폰 MCP 연결
fld distribute <id> [mp4] [type]       — 프로토콜 배포
fld serve [port]                       — MCP 서버
```

## 포트

| 포트 | 서비스 |
|------|--------|
| 8090 | FLD MCP SSE 서버 |
| 8091 | 대시보드 Stats API |
| 8022 | 폰 SSHD (Tailscale) |
| 9999 | 폰 파일 서버 (HTTP PUT) |
