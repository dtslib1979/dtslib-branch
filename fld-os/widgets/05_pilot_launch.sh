#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 5: Pilot Launch — Candidate 승격 후 최소 실행

FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"

echo "🧪 FLD Pilot Launch — $(date '+%H:%M:%S')"
echo "━━━━━━━━━━━━━━━━"

python3 -c "
import sys
sys.path.insert(0, '$FLD_OS_DIR/core')
from ledger import get_ledger

l = get_ledger()
candidates = l.list_by_state('candidate')

if not candidates:
    print('⚠️  Candidate 없음')
    print('💡 먼저 seed→scenario→candidate 전이 필요')
    sys.exit(0)

print(f'🔍 Candidate: {len(candidates)}개')
print('')

ready = [c for c in candidates if c.score >= 30]
print(f'🧪 Pilot 전환 가능 (score≥30): {len(ready)}개')
print('')

for c in candidates:
    status = '✅ 가능' if c.score >= 30 else f'❌ {30-c.score}점 부족'
    print(f'  [{c.score:2d}/50] {c.account:10s} {c.title[:50]}...')
    print(f'         {status} | ID: {c.id}')
    print('')

# 점수 평가 필요 목록
unscored = [c for c in candidates if c.score == 0]
if unscored:
    print(f'⚠️  평가 필요 (score=0): {len(unscored)}개')
    for u in unscored[:3]:
        print(f'  · {u.title[:50]}...')
    print('')
    print('💡 점수 평가: fld score <ID>')
print('💡 Pilot 전환: fld state <ID> pilot')
"

echo ""
echo "✅ Pilot Launch 조회 완료"
