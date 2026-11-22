#!/bin/bash
[ -n "${SEROBEYINN_INVOKED_BY:-}" ] && exit 0
# Detach a pre-compaction flush without changing live session state.

SEROBEYINN_HOOK_DIR=$(CDPATH= cd "$(dirname "$0")" 2>/dev/null && pwd)
. "$SEROBEYINN_HOOK_DIR/lib.sh" 2>/dev/null || exit 0

SEROBEYINN_HOOK_INPUT="$SEROBEYINN_STATE_DIR/hookin-$$.json"
umask 077
if ! cat > "$SEROBEYINN_HOOK_INPUT" 2>/dev/null; then
  rm -f "$SEROBEYINN_HOOK_INPUT" 2>/dev/null || :
  SEROBEYINN_HOOK_INPUT=""
fi

if [ -n "$SEROBEYINN_HOOK_INPUT" ]; then
  if command -v python3 >/dev/null 2>&1; then
    nohup python3 "$SEROBEYINN_PROJECT_DIR/.claude/scripts/flush.py" \
      --hook-input "$SEROBEYINN_HOOK_INPUT" --reason precompact >/dev/null 2>&1 &
  else
    serobeyinn_mark_python_missing
    rm -f "$SEROBEYINN_HOOK_INPUT" 2>/dev/null || :
    serobeyinn_emit PreCompact 'SeroBeyinn sıkıştırma öncesi özeti başlatılamadı: python3 bulunamadı. serobeyinn-doktor çalıştır.'
  fi
fi
exit 0
