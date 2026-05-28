#!/usr/bin/env bash
# Agent health check. Run at the start of a session to verify the
# environment is intact before doing actual research work.
#
# Exits non-zero if any precondition fails. Output is structured for
# both human reading and grep'ing in session logs.

set -u
cd "$(dirname "$0")/.."

fail=0
pass() { echo "ok   $1"; }
warn() { echo "warn $1"; }
err()  { echo "FAIL $1"; fail=1; }

# 1. Repo invariants
[ -d .git ] || err "not inside a git repo"
[ -f CLAUDE.md ] || err "CLAUDE.md missing"
[ -f sources-wishlist.txt ] || err "sources-wishlist.txt missing"

# 2. Branch — protocol says both autonomous and interactive sessions work on main
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [ "$branch" = "main" ]; then
    pass "on main"
else
    warn "on branch '$branch' — protocol expects main (see shared-branch rule in CLAUDE.md)"
fi

# 3. Hook installed
if [ -x .claude/hooks/session-start.sh ]; then
    pass "session-start hook present and executable"
else
    warn "session-start hook missing or not executable"
fi

# 4. Signing workaround in effect (harness signing service has been returning 400)
sign=$(git config --get commit.gpgsign 2>/dev/null || echo "")
if [ "$sign" = "false" ]; then
    pass "commit.gpgsign=false at repo scope (workaround in effect)"
else
    warn "commit.gpgsign=$sign — commits may fail if /tmp/code-sign is down"
fi

# 5. sources-raw/ is populated and readable
raw_count=$(find sources-raw -maxdepth 1 -type f ! -name 'README.md' 2>/dev/null | wc -l | tr -d ' ')
if [ "$raw_count" -gt 0 ]; then
    pass "sources-raw/ has $raw_count primary-source file(s)"
else
    warn "sources-raw/ is empty — nothing to read this session"
fi

# 6. Bank shape (the four canonical directories exist and are non-empty)
for d in sources claim-evidence leads digests; do
    n=$(find "$d" -maxdepth 1 -type f -name '*.md' ! -name 'README.md' 2>/dev/null | wc -l | tr -d ' ')
    if [ "$n" -gt 0 ]; then
        pass "$d/ has $n entry/entries"
    else
        warn "$d/ is empty"
    fi
done

# 7. Index generator present
if [ -x bin/build-index.sh ]; then
    pass "bin/build-index.sh present and executable"
else
    err "bin/build-index.sh missing or not executable"
fi

echo
if [ "$fail" -eq 0 ]; then
    echo "health-check: OK"
    exit 0
else
    echo "health-check: FAILED"
    exit 1
fi
