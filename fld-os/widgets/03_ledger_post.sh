#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 3: Ledger Post — 새 아이템 직접 등록 (Termux:Dialog)
# 대화상자로 입력받아 FLD Seed 생성

FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"

# Termux:Dialog 확인
if ! command -v termux-dialog &>/dev/null; then
    echo "❌ termux-dialog 필요: pkg install termux-dialog"
    exit 1
fi

echo "📝 FLD Ledger Post"
echo "━━━━━━━━━━━━━━━━"

# 제목 입력
TITLE=$(termux-dialog text -t "제목 (80자 내)" -i "" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('text',''))" 2>/dev/null)
[ -z "$TITLE" ] && echo "❌ 취소됨" && exit 1

# 내용 입력
CONTENT=$(termux-dialog text -t "내용/동기 (200자)" -i "" -m 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('text',''))" 2>/dev/null)

# 계정 선택
ACCOUNT=$(termux-dialog radio -t "계정군 선택" -v "person,space,revenue,channel,content,tool,risk,asset" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('text',''))" 2>/dev/null)
[ -z "$ACCOUNT" ] && ACCOUNT="uncategorized"

# FLD Ledger에 등록
python3 -c "
import sys
sys.path.insert(0, '$FLD_OS_DIR/core')
from ledger import get_ledger
l = get_ledger()
item = l.add(
    title='$TITLE',
    motive='$CONTENT',
    account='$ACCOUNT',
    next_action='시나리오 검토'
)
print(f'✅ 등록 완료: {item.id}')
print(f'   [{item.account}] {item.title[:60]}')
print(f'   상태: {item.state}')
"

echo ""
echo "✅ Post 완료"
