# DTSLIB HQ OS 구축 실행 계획서

> Claude Desktop + MCP를 활용한 일괄 작업 인스트럭션
>
> 작성일: 2026-01-16
> 대상: 4개 레포 (HQ + 3개 Cell) 동시 구축

---

## 개요

### 목표
```
dtslib-branch (HQ)  ←→  koosy (Cell)
                    ←→  gohsy (Cell)
                    ←→  papafly (Cell)
```

4개 레포를 HQ OS 시스템으로 연결하여 프랜차이즈 운영체제 구축

### 소요 시간
- 예상: 30분
- MCP 설정 포함: 40분

---

## Part 1: 사전 준비

### 1.1 Claude Desktop 설치 확인
```bash
# macOS
ls /Applications/Claude.app

# Windows
# Claude Desktop 설치 확인
```

### 1.2 MCP 설정 (claude_desktop_config.json)

**macOS 경로:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows 경로:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**설정 내용:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/YOUR_USERNAME/Projects/dtslib"
      ]
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

### 1.3 GitHub PAT 생성

1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. **Token name:** `DTSLIB-HQ-MCP`
3. **Repository access:** `dtslib1979/dtslib-branch`, `dtslib1979/koosy`, `dtslib1979/gohsy`, `dtslib1979/papafly`
4. **Permissions:**
   - Contents: Read and write
   - Pull requests: Read and write
   - Workflows: Read and write
   - Metadata: Read

### 1.4 작업 디렉토리 생성
```bash
mkdir -p ~/Projects/dtslib
cd ~/Projects/dtslib
```

### 1.5 레포지토리 Clone
```bash
# HQ
git clone https://github.com/dtslib1979/dtslib-branch.git

# Cells
git clone https://github.com/dtslib1979/koosy.git
git clone https://github.com/dtslib1979/gohsy.git

# papafly가 없으면 생성 필요
# GitHub에서 새 레포 생성 후:
git clone https://github.com/dtslib1979/papafly.git
```

**디렉토리 구조 확인:**
```
~/Projects/dtslib/
├── dtslib-branch/    # HQ
├── koosy/            # Cell 1
├── gohsy/            # Cell 2
└── papafly/          # Cell 3 (Canary)
```

---

## Part 2: Claude Desktop 프롬프트

### 2.1 세션 시작 프롬프트

Claude Desktop을 열고 다음을 입력:

```
나는 DTSLIB HQ OS 시스템을 구축하려고 해.

작업 디렉토리: ~/Projects/dtslib/

레포지토리 4개:
1. dtslib-branch (HQ 본사)
2. koosy (Cell - Content)
3. gohsy (Cell - Business)
4. papafly (Cell - Product, Canary)

목표:
- HQ에서 모든 Cell을 관리하는 프랜차이즈 시스템 구축
- 각 Cell에 HQ 연결 설정 추가
- Ledger 기반 감사 추적
- Canary Deploy 체계

filesystem MCP로 파일을 직접 읽고 쓸 수 있어.

지금부터 일괄 작업을 시작해줘.
```

---

## Part 3: HQ 확인 및 보완

### 3.1 HQ 현재 상태 확인

```
dtslib-branch/hq/ 디렉토리 구조를 확인해줘.
이미 구축된 파일들이 있는지 체크하고,
빠진 부분이 있으면 알려줘.
```

### 3.2 HQ 필수 파일 체크리스트

| 파일 | 용도 | 상태 |
|------|------|------|
| `hq/registry/branches.json` | Cell 등기부 | ☐ |
| `hq/registry/policy.json` | 정책 | ☐ |
| `hq/registry/decision-engine.json` | 4모드 엔진 | ☐ |
| `hq/registry/owners.json` | 소유권 | ☐ |
| `hq/ledger/ledger.jsonl` | 원장 | ☐ |
| `hq/sync/sync-plan.json` | Canary 전략 | ☐ |
| `hq/sync/conflict-policy.json` | 충돌 정책 | ☐ |
| `hq/billing/cost-policy.json` | 비용 정책 | ☐ |
| `hq/notifications/channels.json` | 알림 채널 | ☐ |
| `hq/notifications/rules.json` | 알림 규칙 | ☐ |
| `hq/recovery/health-check.json` | 헬스체크 | ☐ |
| `hq/dashboard/index.html` | 대시보드 | ☐ |

### 3.3 branches.json 업데이트

**HQ의 branches.json에 3개 Cell이 모두 등록되어 있는지 확인:**

```json
{
  "version": "2.1",
  "hqProtocolVersion": "2.1",
  "cells": [
    {
      "id": "papafly",
      "name": "PAPAFLY",
      "repo": "dtslib1979/papafly",
      "domain": "papafly.dtslib.com",
      "area": "product",
      "tier": "canary",
      "visibility": "private",
      "status": "active",
      "owner": "dimas@dtslib.com",
      "hqProtocolVersion": "2.1",
      "maintenanceMode": false
    },
    {
      "id": "koosy",
      "name": "KOOSY",
      "repo": "dtslib1979/koosy",
      "domain": "koosy.dtslib.com",
      "area": "content",
      "tier": "standard",
      "visibility": "public",
      "status": "active",
      "owner": "dimas@dtslib.com",
      "hqProtocolVersion": "2.1",
      "maintenanceMode": false
    },
    {
      "id": "gohsy",
      "name": "GOHSY",
      "repo": "dtslib1979/gohsy",
      "domain": "gohsy.dtslib.com",
      "area": "business",
      "tier": "standard",
      "visibility": "private",
      "status": "pending",
      "owner": "dimas@dtslib.com",
      "hqProtocolVersion": "2.1",
      "maintenanceMode": false
    }
  ]
}
```

---

## Part 4: Cell 일괄 설정

### 4.1 Cell 공통 파일 생성 프롬프트

```
이제 각 Cell 레포에 HQ 연결 파일을 추가해줘.

각 Cell (koosy, gohsy, papafly)에 다음 파일들을 생성:

1. .hq/manifest.json
2. .github/workflows/hq-upstream.yml

Cell별로 manifest.json의 cellId, tier만 다르게 설정해줘.
```

### 4.2 Cell별 manifest.json

**papafly/.hq/manifest.json (Canary)**
```json
{
  "cellId": "papafly",
  "hqRepo": "dtslib1979/dtslib-branch",
  "hqProtocolVersion": "2.1",
  "tier": "canary",
  "area": "product",
  "syncEnabled": true,
  "reportInterval": "hourly",
  "createdAt": "2026-01-16T00:00:00Z",
  "owner": "dimas@dtslib.com"
}
```

**koosy/.hq/manifest.json (Standard)**
```json
{
  "cellId": "koosy",
  "hqRepo": "dtslib1979/dtslib-branch",
  "hqProtocolVersion": "2.1",
  "tier": "standard",
  "area": "content",
  "syncEnabled": true,
  "reportInterval": "hourly",
  "createdAt": "2026-01-16T00:00:00Z",
  "owner": "dimas@dtslib.com"
}
```

**gohsy/.hq/manifest.json (Standard)**
```json
{
  "cellId": "gohsy",
  "hqRepo": "dtslib1979/dtslib-branch",
  "hqProtocolVersion": "2.1",
  "tier": "standard",
  "area": "business",
  "syncEnabled": true,
  "reportInterval": "hourly",
  "createdAt": "2026-01-16T00:00:00Z",
  "owner": "dimas@dtslib.com"
}
```

### 4.3 Cell 공통 워크플로우

**모든 Cell의 .github/workflows/hq-upstream.yml:**
```yaml
name: HQ Upstream Report

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Load manifest
        id: manifest
        run: |
          if [ -f .hq/manifest.json ]; then
            CELL_ID=$(jq -r '.cellId' .hq/manifest.json)
            HQ_REPO=$(jq -r '.hqRepo' .hq/manifest.json)
            TIER=$(jq -r '.tier' .hq/manifest.json)
            echo "cell_id=$CELL_ID" >> $GITHUB_OUTPUT
            echo "hq_repo=$HQ_REPO" >> $GITHUB_OUTPUT
            echo "tier=$TIER" >> $GITHUB_OUTPUT
          else
            echo "::warning::No manifest found, skipping report"
            exit 0
          fi

      - name: Collect metrics
        id: metrics
        run: |
          echo "commits=$(git rev-list --count HEAD)" >> $GITHUB_OUTPUT
          echo "last_commit=$(git log -1 --format=%H)" >> $GITHUB_OUTPUT
          echo "last_commit_date=$(git log -1 --format=%cI)" >> $GITHUB_OUTPUT

      - name: Report to HQ
        if: steps.manifest.outputs.cell_id != ''
        env:
          GH_TOKEN: ${{ secrets.HQ_REPORT_TOKEN }}
        run: |
          if [ -z "$GH_TOKEN" ]; then
            echo "::warning::HQ_REPORT_TOKEN not set, skipping report"
            exit 0
          fi

          curl -X POST \
            -H "Authorization: token $GH_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/${{ steps.manifest.outputs.hq_repo }}/dispatches" \
            -d '{
              "event_type": "cell-report",
              "client_payload": {
                "cell": "${{ steps.manifest.outputs.cell_id }}",
                "tier": "${{ steps.manifest.outputs.tier }}",
                "repo": "${{ github.repository }}",
                "commits": "${{ steps.metrics.outputs.commits }}",
                "lastCommit": "${{ steps.metrics.outputs.last_commit }}",
                "timestamp": "'$(date -Iseconds)'"
              }
            }'
          echo "Report sent to HQ"
```

---

## Part 5: 일괄 실행 스크립트

### 5.1 전체 작업 프롬프트 (한 번에 실행)

```
다음 작업을 순서대로 실행해줘:

1. papafly 레포에:
   - .hq/manifest.json 생성 (tier: canary)
   - .github/workflows/hq-upstream.yml 생성

2. koosy 레포에:
   - .hq/manifest.json 생성 (tier: standard)
   - .github/workflows/hq-upstream.yml 생성

3. gohsy 레포에:
   - .hq/manifest.json 생성 (tier: standard)
   - .github/workflows/hq-upstream.yml 생성

4. 각 레포에서 git add, commit, push 실행
   - 커밋 메시지: "feat: HQ 연결 설정 추가"

5. HQ(dtslib-branch)의 branches.json 업데이트
   - 3개 Cell 모두 status: "active"로 변경

6. HQ ledger.jsonl에 초기화 기록 추가:
   {"id":"TXN-INIT-001","timestamp":"...","eventType":"system_init","actor":"admin","data":{"cells":["papafly","koosy","gohsy"]},"status":"success"}

7. HQ에서 git add, commit, push 실행
   - 커밋 메시지: "feat: Cell 3개 연결 완료"

모든 작업이 끝나면 결과를 요약해줘.
```

### 5.2 수동 실행 시 명령어

```bash
# === Cell: papafly ===
cd ~/Projects/dtslib/papafly
mkdir -p .hq .github/workflows
# (파일 생성)
git add .
git commit -m "feat: HQ 연결 설정 추가"
git push

# === Cell: koosy ===
cd ~/Projects/dtslib/koosy
mkdir -p .hq .github/workflows
# (파일 생성)
git add .
git commit -m "feat: HQ 연결 설정 추가"
git push

# === Cell: gohsy ===
cd ~/Projects/dtslib/gohsy
mkdir -p .hq .github/workflows
# (파일 생성)
git add .
git commit -m "feat: HQ 연결 설정 추가"
git push

# === HQ: dtslib-branch ===
cd ~/Projects/dtslib/dtslib-branch
# (branches.json 업데이트, ledger 추가)
git add .
git commit -m "feat: Cell 3개 연결 완료"
git push
```

---

## Part 6: 검증

### 6.1 구조 검증 프롬프트

```
모든 레포의 HQ 연결 상태를 검증해줘:

1. 각 Cell의 .hq/manifest.json 존재 확인
2. 각 Cell의 hq-upstream.yml 존재 확인
3. HQ branches.json에 3개 Cell 등록 확인
4. HQ ledger.jsonl에 초기화 기록 확인

결과를 테이블로 보여줘.
```

### 6.2 예상 검증 결과

| 레포 | manifest.json | hq-upstream.yml | HQ 등록 | 상태 |
|------|---------------|-----------------|---------|------|
| papafly | ✅ | ✅ | ✅ canary | 정상 |
| koosy | ✅ | ✅ | ✅ standard | 정상 |
| gohsy | ✅ | ✅ | ✅ standard | 정상 |

### 6.3 GitHub Actions 활성화 확인

각 Cell 레포에서:
1. Settings → Actions → General
2. "Allow all actions and reusable workflows" 선택
3. Workflow permissions → "Read and write permissions" 선택

### 6.4 HQ_REPORT_TOKEN 설정 (선택)

Cell이 HQ에 자동 보고하려면:
1. 각 Cell 레포 → Settings → Secrets → Actions
2. `HQ_REPORT_TOKEN` 추가 (HQ 레포에 dispatch 권한 있는 PAT)

---

## Part 7: 운영 확인

### 7.1 대시보드 확인

```
HQ 대시보드를 브라우저에서 열어볼게:
https://dtslib1979.github.io/dtslib-branch/hq/dashboard/

또는 로컬에서:
open ~/Projects/dtslib/dtslib-branch/hq/dashboard/index.html
```

### 7.2 첫 번째 Sync 테스트

```
HQ에서 papafly로 테스트 sync를 해보자:

1. HQ의 hq/sync/templates/에 테스트 파일 추가
2. papafly에만 PR 생성 (Canary)
3. 성공하면 koosy, gohsy로 확대
```

---

## Part 8: 트러블슈팅

### 8.1 MCP 연결 안 됨

```bash
# Claude Desktop 재시작
# 또는 config 파일 문법 확인
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .
```

### 8.2 Git push 권한 없음

```bash
# SSH 키 확인
ssh -T git@github.com

# 또는 HTTPS + PAT
git remote set-url origin https://YOUR_PAT@github.com/dtslib1979/REPO.git
```

### 8.3 Workflow 실행 안 됨

1. Actions 탭에서 workflow 활성화 확인
2. `.github/workflows/` 경로 정확한지 확인
3. YAML 문법 오류 확인

---

## 요약: 한 줄 명령

Claude Desktop에서 이것만 입력하면 됨:

```
~/Projects/dtslib/ 디렉토리에 4개 레포가 clone되어 있어.
(dtslib-branch, koosy, gohsy, papafly)

각 Cell(koosy, gohsy, papafly)에 .hq/manifest.json과
.github/workflows/hq-upstream.yml을 생성하고,
HQ(dtslib-branch)의 branches.json을 업데이트해서
모든 레포에 커밋/푸시해줘.

tier는 papafly=canary, koosy=standard, gohsy=standard로.
```

**끝.**

---

## Appendix: 파일 템플릿

### A. manifest.json 템플릿
```json
{
  "cellId": "{{CELL_ID}}",
  "hqRepo": "dtslib1979/dtslib-branch",
  "hqProtocolVersion": "2.1",
  "tier": "{{TIER}}",
  "area": "{{AREA}}",
  "syncEnabled": true,
  "reportInterval": "hourly",
  "createdAt": "{{TIMESTAMP}}",
  "owner": "dimas@dtslib.com"
}
```

### B. Cell 값 매핑

| Cell | CELL_ID | TIER | AREA |
|------|---------|------|------|
| papafly | papafly | canary | product |
| koosy | koosy | standard | content |
| gohsy | gohsy | standard | business |

---

*문서 버전: 1.0*
*작성일: 2026-01-16*
*용도: Claude Desktop + MCP 일괄 작업용*
