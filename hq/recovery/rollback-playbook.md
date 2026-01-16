# HQ Rollback Playbook

## 1. Identify the Problem

```bash
# Check recent ledger entries
tail -50 hq/ledger/ledger.jsonl | jq .

# Find failing transaction
grep "failed" hq/ledger/ledger.jsonl | tail -10
```

## 2. Determine Blast Radius

- Which cells are affected?
- What was the change?
- How many users impacted?

## 3. Execute Rollback

### Option A: Revert Last Sync

```bash
# Find last successful sync
git log --oneline hq/sync/ | head -5

# Revert to that commit
git revert <commit-hash>
```

### Option B: Restore from Backup

```bash
# List backup tags
git tag -l "backup/ledger/*" | tail -5

# Restore ledger
git checkout backup/ledger/2026-01-15 -- hq/ledger/ledger.jsonl
```

### Option C: Emergency Kill Switch

```bash
# Edit decision-engine.json
# Set "killSwitch": true

# This will:
# - Halt all automated operations
# - Require manual intervention
# - Log to ledger
```

## 4. Verify Recovery

```bash
# Check cell health
curl https://koosy.dtslib.com/health.json
curl https://gohsy.dtslib.com/health.json
curl https://papafly.dtslib.com/health.json
```

## 5. Post-Mortem

1. Document what happened
2. Record in ledger with `escalation_triggered` event
3. Update policies if needed
4. Notify stakeholders

## Emergency Contacts

- HQ Admin: dimas@dtslib.com
- GitHub Issues: dtslib1979/dtslib-branch/issues
