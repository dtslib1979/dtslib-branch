#!/usr/bin/env bash
# 지사(cell) 부트스트랩 — 본사 templates 를 cell 레포에 install
#
# Usage:
#   ./install-cell.sh <cell_id> <cell_repo> [cell_name]
# 예:
#   ./install-cell.sh koosy dtslib1979/koosy KOOSY
#   ./install-cell.sh buckley dtslib1979/buckleychang.com BUCKLEY
set -euo pipefail

CELL_ID="${1:?cell_id required}"
CELL_REPO="${2:?cell_repo required (owner/repo)}"
CELL_NAME="${3:-${CELL_ID^^}}"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Cell 로컬 경로 추론
CELL_DIR="$HOME/${CELL_REPO##*/}"
[ -d "$CELL_DIR" ] || { echo "❌ $CELL_DIR 없음"; exit 1; }

HQ_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
TEMPLATES="$HQ_DIR/hq/sync/templates"

echo "📦 $CELL_NAME ($CELL_ID) 부트스트랩 시작"
echo "   레포: $CELL_REPO"
echo "   경로: $CELL_DIR"

# 1) .hq/manifest.json
mkdir -p "$CELL_DIR/.hq"
sed -e "s|__CELL_ID__|$CELL_ID|g" \
    -e "s|__CELL_REPO__|$CELL_REPO|g" \
    -e "s|__BOOTSTRAP_TIMESTAMP__|$TS|g" \
    "$TEMPLATES/.hq-manifest.json.template" > "$CELL_DIR/.hq/manifest.json"
echo "  ✅ .hq/manifest.json"

# 2) workflows
mkdir -p "$CELL_DIR/.github/workflows"
cp "$TEMPLATES/hq-receiver.yml.template" "$CELL_DIR/.github/workflows/hq-receiver.yml"
cp "$TEMPLATES/hq-upstream.yml.template" "$CELL_DIR/.github/workflows/hq-upstream.yml"
echo "  ✅ workflows: hq-receiver.yml + hq-upstream.yml"

# 3) backoffice/
mkdir -p "$CELL_DIR/backoffice"
sed -e "s|__CELL_ID__|$CELL_ID|g" \
    -e "s|__CELL_REPO__|$CELL_REPO|g" \
    -e "s|__CELL_NAME__|$CELL_NAME|g" \
    "$TEMPLATES/backoffice/index.html.template" > "$CELL_DIR/backoffice/index.html"
echo "  ✅ backoffice/index.html"

# 4) robots.txt 보강 (백오피스 검색엔진 차단)
if [ -f "$CELL_DIR/robots.txt" ]; then
  if ! grep -q "Disallow: /backoffice" "$CELL_DIR/robots.txt"; then
    echo "" >> "$CELL_DIR/robots.txt"
    echo "Disallow: /backoffice/" >> "$CELL_DIR/robots.txt"
    echo "Disallow: /.hq/" >> "$CELL_DIR/robots.txt"
    echo "  ✅ robots.txt 보강"
  fi
else
  cat > "$CELL_DIR/robots.txt" <<EOF
User-agent: *
Disallow: /backoffice/
Disallow: /.hq/
EOF
  echo "  ✅ robots.txt 신규"
fi

# 5) GitHub Secret HQ_REPORT_TOKEN
GH_TOKEN_SOURCE="${GITHUB_TOKEN:-$(gh auth token 2>/dev/null || echo '')}"
if [ -n "$GH_TOKEN_SOURCE" ]; then
  echo "$GH_TOKEN_SOURCE" | gh secret set HQ_REPORT_TOKEN -R "$CELL_REPO" 2>&1 | tail -1
  echo "  ✅ HQ_REPORT_TOKEN 등록"
else
  echo "  ⚠️ gh 토큰 없음 — secret 등록 skip"
fi

echo "✅ $CELL_NAME 부트스트랩 완료"
