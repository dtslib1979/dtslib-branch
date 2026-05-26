#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 4: Filter — 계정/상태별 아이템 필터링

FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"

echo "🔍 FLD Filter — $(date '+%H:%M:%S')"
echo "━━━━━━━━━━━━━━━━"

python3 -c "
import sys
sys.path.insert(0, '$FLD_OS_DIR/core')
from ledger import get_ledger

l = get_ledger()
stats = l.stats()

print('📊 FLD OS 현황')
print(f'  전체: {stats[\"total\"]}개 | 활성: {stats[\"active\"]}개 | 드롭: {stats[\"dropped\"]}개')
print('')
print('--- 상태별 ---')
for s, c in stats['by_state'].items():
    label = {'seed': '🌱 Seed', 'scenario': '📋 Scenario', 'candidate': '🔍 Candidate', 'pilot': '🧪 Pilot', 'protocol': '📦 Protocol'}.get(s, s)
    bar = '█' * (c // 2 + 1) if c > 0 else '·'
    print(f'  {label}: {c:3d}개 {bar}')
print('')
print('--- 계정군별 ---')
for a, c in stats['by_account'].items():
    if c > 0:
        bar = '█' * (c // 2 + 1)
        print(f'  {a:10s}: {c:3d}개 {bar}')
print('')
print('--- 점수 상위 ---')
scored = [i for i in l.list_active() if i.score > 0]
scored.sort(key=lambda x: x.score, reverse=True)
for s in scored[:5]:
    print(f'  {s.score:2d}/50 [{s.account}] {s.title[:50]}...')
print('')
print('💡 필터 명령:')
print('  fld list <state>     — 상태별 조회')
print('  fld list --account   — 계정별 조회')
"

echo ""
echo "✅ Filter 완료"
