#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 7: Protocol Pack — Protocol 아이템 최종 자산화
# 배포 가능한 형태로 패키징 (Telegram/YouTube)

FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"

echo "📦 FLD Protocol Pack — $(date '+%H:%M:%S')"
echo "━━━━━━━━━━━━━━━━"

python3 -c "
import sys
sys.path.insert(0, '$FLD_OS_DIR/core')
from ledger import get_ledger

l = get_ledger()
protocols = l.list_by_state('protocol')
pilots = l.list_by_state('pilot')

print(f'📦 Protocol: {len(protocols)}개')
print(f'🧪 Pilot (승격 가능): {len(pilots)}개')
print('')

for p in protocols:
    links = p.links or []
    print(f'  [{p.score:2d}/50] {p.title[:50]}...')
    print(f'     자산: {len(links)}개 링크')
    for link in links[:3]:
        print(f'       · {link[:60]}')
    print(f'     배포: fld distribute {p.id} telegram')
    print('')

if pilots:
    ready = [p for p in pilots if p.score >= 30 and p.links]
    print(f'🧪 → 📦 승격 가능: {len(ready)}개')
    for r in ready[:3]:
        print(f'  · {r.title[:50]}... (fld state {r.id} protocol)')

print('')
echo '💡 배포 명령:'
echo '  fld distribute <ID> telegram   — 텔레그램 배포'
echo '  fld distribute <ID> youtube    — 유튜브 배포'
echo '  fld distribute <ID> all        — 전체 채널 배포'
"

echo ""
echo "✅ Protocol Pack 완료"
