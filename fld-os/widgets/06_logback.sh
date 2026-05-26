#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 6: Logback — 변경 이력 및 활동 로그
# 마지막 10개 변경사항 출력

FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"

echo "📜 FLD Logback — $(date '+%H:%M:%S')"
echo "━━━━━━━━━━━━━━━━"

python3 -c "
import json
from pathlib import Path
from datetime import datetime

ledger_path = '$FLD_OS_DIR/data/ledger.jsonl'

if not Path(ledger_path).exists():
    print('⚠️ Ledger 파일 없음')
    sys.exit(0)

items = []
with open(ledger_path) as f:
    for line in f:
        line = line.strip()
        if line:
            items.append(json.loads(line))

# 최근 업데이트 순 정렬
items.sort(key=lambda x: x.get('updated_at', ''), reverse=True)

print(f'📊 총 {len(items)}개 항목')
print('')
print('--- 최근 변경 10개 ---')
for item in items[:10]:
    state_icon = {'seed': '🌱', 'scenario': '📋', 'candidate': '🔍', 'pilot': '🧪', 'protocol': '📦'}.get(item.get('state', ''), '·')
    updated = item.get('updated_at', '')[:19].replace('T', ' ')
    history = item.get('history', [])
    last = history[-1].get('by', 'system') if history else 'system'
    print(f'  {state_icon} [{item.get(\"state\",\"?\")}] {item.get(\"title\",\"\")[:55]}...')
    print(f'     {updated} | {last} | {item.get(\"account\",\"uncategorized\")}')
    print('')
"

echo ""
echo "✅ Logback 완료"
