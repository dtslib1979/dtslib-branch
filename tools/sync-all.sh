#!/bin/bash
# DTSLIB HQ - 전체 레포 동기화
# 사용법: bash ~/dtslib-branch/tools/sync-all.sh

echo "========================================"
echo "  DTSLIB HQ - 전체 레포 동기화"
echo "========================================"
echo ""

repos=("dtslib-branch" "koosy" "gohsy" "artrew" "papafly" "buckley")

for repo in "${repos[@]}"; do
  echo "📦 $repo"
  if [ -d ~/"$repo" ]; then
    cd ~/"$repo"
    git pull 2>&1 | sed 's/^/   /'
  else
    echo "   ⚠️  레포 없음 - 클론 시도..."
    gh repo clone "dtslib1979/$repo" ~/"$repo" 2>&1 | sed 's/^/   /'
  fi
  echo ""
done

echo "========================================"
echo "  동기화 완료"
echo "========================================"
