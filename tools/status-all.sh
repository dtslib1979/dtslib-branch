#!/bin/bash
# DTSLIB HQ - 전체 레포 상태 확인
# 사용법: bash ~/dtslib-branch/tools/status-all.sh

echo "========================================"
echo "  DTSLIB HQ - 전체 레포 상태"
echo "========================================"
echo ""

repos=("dtslib-branch" "koosy" "gohsy" "papafly")

for repo in "${repos[@]}"; do
  echo "📦 $repo"
  if [ -d ~/"$repo" ]; then
    cd ~/"$repo"
    branch=$(git branch --show-current 2>/dev/null)
    echo "   브랜치: $branch"

    status=$(git status -s 2>/dev/null)
    if [ -z "$status" ]; then
      echo "   상태: ✅ 클린"
    else
      echo "   상태: ⚠️  변경사항 있음"
      echo "$status" | sed 's/^/   /'
    fi

    # 원격과 비교
    git fetch origin --quiet 2>/dev/null
    ahead=$(git rev-list --count origin/$branch..HEAD 2>/dev/null)
    behind=$(git rev-list --count HEAD..origin/$branch 2>/dev/null)

    if [ "$ahead" -gt 0 ] 2>/dev/null; then
      echo "   ↑ $ahead 커밋 push 필요"
    fi
    if [ "$behind" -gt 0 ] 2>/dev/null; then
      echo "   ↓ $behind 커밋 pull 필요"
    fi
  else
    echo "   ❌ 레포 없음"
  fi
  echo ""
done

echo "========================================"
