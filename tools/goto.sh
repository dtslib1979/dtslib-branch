#!/bin/bash
# DTSLIB HQ - 빠른 레포 이동
# 사용법: source ~/dtslib-branch/tools/goto.sh [레포명]
# 또는 alias 등록 후: goto koosy

show_help() {
  echo "DTSLIB HQ - 빠른 레포 이동"
  echo ""
  echo "사용법: source ~/dtslib-branch/tools/goto.sh [레포명]"
  echo ""
  echo "레포 목록:"
  echo "  hq, branch    → ~/dtslib-branch (본사)"
  echo "  koosy         → ~/koosy"
  echo "  gohsy         → ~/gohsy"
  echo "  papafly       → ~/papafly"
  echo ""
  echo "팁: .bashrc에 다음 추가"
  echo "  goto() { source ~/dtslib-branch/tools/goto.sh \$1; }"
}

case $1 in
  hq|branch|dtslib)
    cd ~/dtslib-branch && echo "📍 dtslib-branch (HQ)"
    ;;
  koosy)
    cd ~/koosy 2>/dev/null && echo "📍 koosy" || echo "❌ ~/koosy 없음"
    ;;
  gohsy)
    cd ~/gohsy 2>/dev/null && echo "📍 gohsy" || echo "❌ ~/gohsy 없음"
    ;;
  papafly)
    cd ~/papafly 2>/dev/null && echo "📍 papafly" || echo "❌ ~/papafly 없음"
    ;;
  -h|--help|help)
    show_help
    ;;
  *)
    show_help
    ;;
esac
