#!/bin/bash
[ -n "${SEROBEYINN_INVOKED_BY:-}" ] && exit 0
# Mark relational-memory debt, then detach the automatic session flush.

SEROBEYINN_HOOK_DIR=$(CDPATH= cd "$(dirname "$0")" 2>/dev/null && pwd)
. "$SEROBEYINN_HOOK_DIR/lib.sh" 2>/dev/null || exit 0

SEROBEYINN_HOOK_INPUT="$SEROBEYINN_STATE_DIR/hookin-$$.json"
umask 077
if ! cat > "$SEROBEYINN_HOOK_INPUT" 2>/dev/null; then
  rm -f "$SEROBEYINN_HOOK_INPUT" 2>/dev/null || :
  SEROBEYINN_HOOK_INPUT=""
fi

SEROBEYINN_SESSION_KEY=""
if [ -n "$SEROBEYINN_HOOK_INPUT" ]; then
  SEROBEYINN_SESSION_KEY=$(serobeyinn_session_key < "$SEROBEYINN_HOOK_INPUT" 2>/dev/null || :)
fi

SEROBEYINN_MEMORY_DIR="$SEROBEYINN_PROJECT_DIR/🔮 850-Companion"
SEROBEYINN_START=0
SEROBEYINN_PROMPTS=0
SEROBEYINN_SESSION_START_FILE=""
SEROBEYINN_PROMPT_COUNT_FILE=""
SEROBEYINN_REFLECTION_FILE=""
if [ -n "$SEROBEYINN_SESSION_KEY" ]; then
  SEROBEYINN_SESSION_START_FILE="$SEROBEYINN_STATE_DIR/session_start_time.$SEROBEYINN_SESSION_KEY"
  SEROBEYINN_PROMPT_COUNT_FILE="$SEROBEYINN_STATE_DIR/prompt_count.$SEROBEYINN_SESSION_KEY"
  SEROBEYINN_REFLECTION_FILE="$SEROBEYINN_STATE_DIR/needs_reflection.$SEROBEYINN_SESSION_KEY"
  [ -f "$SEROBEYINN_SESSION_START_FILE" ] && SEROBEYINN_START=$(sed -n '1p' "$SEROBEYINN_SESSION_START_FILE" 2>/dev/null || :)
  [ -f "$SEROBEYINN_PROMPT_COUNT_FILE" ] && SEROBEYINN_PROMPTS=$(sed -n '1p' "$SEROBEYINN_PROMPT_COUNT_FILE" 2>/dev/null || :)
fi
case "$SEROBEYINN_START" in ''|*[!0-9]*) SEROBEYINN_START=0 ;; esac
case "$SEROBEYINN_PROMPTS" in ''|*[!0-9]*) SEROBEYINN_PROMPTS=0 ;; esac

SEROBEYINN_MODIFIED=0
if [ -f "$SEROBEYINN_MEMORY_DIR/Last-Session.md" ]; then
  SEROBEYINN_FILE_MTIME=$(serobeyinn_mtime "$SEROBEYINN_MEMORY_DIR/Last-Session.md")
  case "$SEROBEYINN_FILE_MTIME" in ''|*[!0-9]*) SEROBEYINN_FILE_MTIME=0 ;; esac
  [ "$SEROBEYINN_FILE_MTIME" -gt "$SEROBEYINN_START" ] 2>/dev/null && SEROBEYINN_MODIFIED=1
fi

if [ "$SEROBEYINN_PROMPTS" -ge 5 ] && [ "$SEROBEYINN_MODIFIED" -eq 0 ] && [ -n "$SEROBEYINN_REFLECTION_FILE" ]; then
  printf 'Oturum hafıza güncellemeden bitti. Prompt: %s. %s\n' \
    "$SEROBEYINN_PROMPTS" "$(date '+%Y-%m-%d %H:%M' 2>/dev/null)" \
    > "$SEROBEYINN_REFLECTION_FILE" 2>/dev/null || :
fi

if [ -n "$SEROBEYINN_HOOK_INPUT" ]; then
  if command -v python3 >/dev/null 2>&1; then
    nohup python3 "$SEROBEYINN_PROJECT_DIR/.claude/scripts/flush.py" \
      --hook-input "$SEROBEYINN_HOOK_INPUT" >/dev/null 2>&1 &
  else
    serobeyinn_mark_python_missing
    rm -f "$SEROBEYINN_HOOK_INPUT" 2>/dev/null || :
    serobeyinn_emit SessionEnd 'SeroBeyinn arka plan özeti başlatılamadı: python3 bulunamadı. serobeyinn-doktor çalıştır.'
  fi
fi

[ -n "$SEROBEYINN_SESSION_START_FILE" ] && rm -f "$SEROBEYINN_SESSION_START_FILE" 2>/dev/null || :
[ -n "$SEROBEYINN_PROMPT_COUNT_FILE" ] && rm -f "$SEROBEYINN_PROMPT_COUNT_FILE" 2>/dev/null || :
exit 0
