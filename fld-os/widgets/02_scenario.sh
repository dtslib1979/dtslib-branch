#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 2: Scenario — Seed 목록 조회 및 시나리오 전환

FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"

echo "📋 FLD Scenario — $(date '+%H:%M:%S')"
echo "━━━━━━━━━━━━━━━━"

python3 -c "
import sys
sys.path.insert(0, '$FLD_OS_DIR/core')
from ledger import get_ledger

l = get_ledger()
seeds = l.list_by_state('seed')
scenarios = l.list_by_state('scenario')

print(f'🌱 Seed: {len(seeds)}개')
print(f'📋 Scenario: {len(scenarios)}개')
print('')
print('--- Seed 목록 (시나리오 전환 가능) ---')
for i, s in enumerate(seeds[:10], 1):
    print(f'{i}. [{s.account}] {s.title[:60]}...')
    print(f'   ID: {s.id}')
    print(f'   원천: {s.raw_source[:40] if s.raw_source else \"없음\"}')
    print('')

if len(seeds) > 10:
    print(f'   ... 외 {len(seeds)-10}개')
print('')
print('💡 시나리오 전환: fld state <ID> scenario')
"

echo ""
echo "✅ Scenario 조회 완료"
