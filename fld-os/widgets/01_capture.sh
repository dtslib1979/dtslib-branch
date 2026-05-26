#!/data/data/com.termux/files/usr/bin/bash
# FLD OS Widget 1: Capture — Parksy 로그 수집 → Seed 등록
# Termux:Widget 실행용 (bash)
# 사용법: termux-widget 호출 또는 직접 실행

PHONE_IP="${PHONE_IP:-$(cat ~/.phone_ip 2>/dev/null || echo '100.103.250.45')}"
FLD_OS_DIR="${FLD_OS_DIR:-~/dtslib-branch/fld-os}"
PARKSY_LOGS_DIR="${PARKSY_LOGS_DIR:-~/uploads/parksy-logs-phone/parksy-logs}"

echo "📸 FLD Capture — $(date '+%H:%M:%S')"
echo "━━━━━━━━━━━━━━━━"

# 1. 최신 로그 파일 확인
if [ -d "$PARKSY_LOGS_DIR" ]; then
    LATEST=$(ls -t "$PARKSY_LOGS_DIR"/ParksyLog_*.md 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        echo "📄 최신 로그: $(basename "$LATEST")"
        echo "   크기: $(wc -c < "$LATEST") 바이트"
        echo "   첫줄: $(head -1 "$LATEST")"
    else
        echo "⚠️  로그 파일 없음"
    fi
else
    echo "⚠️  로그 디렉토리 없음"
fi

# 2. FLD ingest 실행
python3 "$FLD_OS_DIR/integration/parksy_watcher.py" scan 2>&1

# 3. 현재 Seed 목록
echo ""
echo "📊 Seed 현황:"
python3 -c "
import json, sys
sys.path.insert(0, '$FLD_OS_DIR/core')
from ledger import get_ledger
l = get_ledger()
seeds = l.list_by_state('seed')
for s in seeds[:5]:
    print(f'  [{s.account}] {s.title[:50]}...')
print(f'  ... 총 {len(seeds)}개 Seed')
"
echo ""
echo "✅ Capture 완료"
