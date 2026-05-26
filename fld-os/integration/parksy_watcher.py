#!/usr/bin/env python3
"""
Parksy Capture Watcher — 로그 파일 자동 감시 → FLD Seed Ingestion

parksy-logs 디렉토리를 감시하다 새 로그 파일이 생성되면
FLD OS ledger에 Seed로 자동 등록.

모드:
  - watch: inotify-based 실시간 감시 (python3 -m inotify 필요)
  - scan: 기존 파일 전체 스캔
  - once: 단일 파일 처리
"""
import json, os, re, sys, time, hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── 설정 ───
LOGS_DIR = Path(os.environ.get("PARKSY_LOGS_DIR",
    str(Path.home() / "uploads" / "parksy-logs-phone" / "parksy-logs")))
FLD_LEDGER = Path(os.environ.get("FLD_LEDGER_PATH",
    str(Path.home() / "dtslib-branch" / "fld-os" / "data" / "ledger.jsonl")))

# 중복 방지: 이미 처리된 파일 추적
SEEN_FILE = Path(os.environ.get("WATCHER_SEEN_FILE",
    str(Path.home() / "dtslib-branch" / "fld-os" / "data" / ".watcher_seen.json")))


def _load_seen() -> set:
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text()))
        except Exception:
            pass
    return set()


def _save_seen(seen: set):
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(list(seen), ensure_ascii=False))


def _parse_log_for_seed(log_path: Path) -> Optional[dict]:
    """로그 파일에서 FLD Seed Item 추출"""
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠️  읽기 실패 {log_path.name}: {e}")
        return None

    if not text.strip():
        return None

    # 메타데이터 추출 (frontmatter)
    date_str = ""
    source = ""
    fm_match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        date_m = re.search(r'date:\s*(.+)', fm)
        source_m = re.search(r'source:\s*(.+)', fm)
        if date_m:
            date_str = date_m.group(1).strip()
        if source_m:
            source = source_m.group(1).strip()

    # 제목 추출: 첫 100자
    body = text[fm_match.end():] if fm_match else text
    title = body.strip()[:100].replace("\n", " ")
    if len(title) > 80:
        title = title[:77] + "..."

    # 화자 분리 (첫 문장)
    first_sentences = re.findall(r'(?m)^([A-Z가-힣].+?[.!?])\s*$', body[:500])
    motive = first_sentences[0][:200] if first_sentences else title[:200]

    # 대화 길이 (글자 수)
    char_count = len(body.strip())

    # 계정 분류 휴리스틱
    account = "uncategorized"
    title_lower = title.lower()
    if any(k in title_lower for k in ["요리", "레시피", "음식", "셰프", "맛집", "식당"]):
        account = "person"
    elif any(k in title_lower for k in ["음악", "트렌드", "문화", "예술", "힙합"]):
        account = "content"
    elif any(k in title_lower for k in ["태블릿", "워크스테이션", "방송", "장비", "키트"]):
        account = "tool"
    elif any(k in title_lower for k in ["사업", "비즈니스", "수익", "매출", "ip"]):
        account = "revenue"
    elif any(k in title_lower for k in ["심리", "정신", "인지", "철학", "자아"]):
        account = "person"

    # 공간 추출
    space = source if source else "unknown"

    # 채널 추출
    channel = source if source else "file"

    # 태그 생성
    tags = ["parksy-capture", f"source:{source}"]
    if char_count > 10000:
        tags.append("long-form")
    if "?" in title:
        tags.append("inquiry")

    seed = {
        "id": f"FLD-{int(time.time())}-{hashlib.md5(log_path.name.encode()).hexdigest()[:6]}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "state": "seed",
        "title": title,
        "raw_source": str(log_path),
        "actor": "",
        "space": space,
        "motive": motive,
        "output_guess": "",
        "revenue_guess": "",
        "channel": channel,
        "risk": "",
        "next_action": "시나리오 검토",
        "account": account,
        "score": 0,
        "score_detail": {},
        "tags": tags,
        "history": [{"state": "seed", "at": datetime.now(timezone.utc).isoformat(), "by": "parksy_watcher"}],
        "links": [],
        "notes": f"Auto-ingested from {log_path.name} ({char_count}자)",
        "dropped": False,
        "drop_reason": "",
    }
    return seed


def ingest_file(log_path: Path, force: bool = False) -> Optional[dict]:
    """파일 1개를 FLD Seed로 등록"""
    seen = _load_seen()
    file_key = str(log_path.absolute())

    if file_key in seen and not force:
        print(f"  ⏭️  {log_path.name} — 이미 처리됨")
        return None

    seed = _parse_log_for_seed(log_path)
    if not seed:
        print(f"  ⚠️  {log_path.name} — 파싱 불가 (빈 파일)")
        return None

    # FLD Ledger에 추가
    FLD_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(str(FLD_LEDGER), "a") as f:
        f.write(json.dumps(seed, ensure_ascii=False) + "\n")

    seen.add(file_key)
    _save_seen(seen)

    print(f"  ✅ {log_path.name} → Seed [{seed['account']}] {seed['title'][:60]}...")
    return seed


def scan_all(force: bool = False) -> list:
    """logs 디렉토리 전체 스캔"""
    if not LOGS_DIR.exists():
        print(f"  ❌ 로그 디렉토리 없음: {LOGS_DIR}")
        return []

    md_files = sorted(LOGS_DIR.glob("ParksyLog_*.md"))
    print(f"  📂 {len(md_files)}개 로그 파일 발견")

    results = []
    for fpath in md_files:
        result = ingest_file(fpath, force=force)
        if result:
            results.append(result)

    print(f"\n  📊 총 {len(results)}개 Seed 등록됨")
    return results


def watch_loop(interval: int = 30):
    """폴링 기반 감시 루프 (inotify 대체)"""
    print(f"  👀 Watcher 시작: {LOGS_DIR} (interval={interval}s)")
    print(f"  💾 Ledger: {FLD_LEDGER}")
    print(f"  📋 Seen: {SEEN_FILE}")

    while True:
        scan_all()
        time.sleep(interval)


# ─── CLI ───
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    force = "--force" in sys.argv or "-f" in sys.argv

    if cmd == "scan":
        results = scan_all(force=force)
        print(json.dumps({
            "ingested": len(results),
            "seeds": [r["id"] for r in results],
        }, ensure_ascii=False, indent=2))

    elif cmd == "watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 30
        watch_loop(interval)

    elif cmd == "once":
        fpath = sys.argv[2] if len(sys.argv) > 2 else ""
        if fpath:
            r = ingest_file(Path(fpath), force=force)
            print(json.dumps(r or {"error": "ingest failed"}, ensure_ascii=False, indent=2))
        else:
            print("Usage: parksy_watcher.py once <file_path>")

    else:
        print(f"Usage: {sys.argv[0]} [scan|watch|once] [options]")
        print(f"  scan            — 기존 로그 전체 스캔")
        print(f"  watch [interval] — 실시간 감시 (기본 30s)")
        print(f"  once <path>     — 단일 파일 처리")
        print(f"  -f, --force     — 중복 무시 강제 처리")
