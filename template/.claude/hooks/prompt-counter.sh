#!/bin/bash
[ -n "${SEROBEYINN_INVOKED_BY:-}" ] && exit 0
# Count prompts and nudge at every multiple of fifteen.

SEROBEYINN_HOOK_DIR=$(CDPATH= cd "$(dirname "$0")" 2>/dev/null && pwd)
. "$SEROBEYINN_HOOK_DIR/lib.sh" 2>/dev/null || exit 0

SEROBEYINN_SESSION_KEY=$(serobeyinn_session_key 2>/dev/null || :)
[ -n "$SEROBEYINN_SESSION_KEY" ] || exit 0

SEROBEYINN_PROMPT_COUNT_FILE="$SEROBEYINN_STATE_DIR/prompt_count.$SEROBEYINN_SESSION_KEY"
SEROBEYINN_LOCK_DIR="$SEROBEYINN_PROMPT_COUNT_FILE.lock"
SEROBEYINN_LOCK_ATTEMPT=0
while ! mkdir "$SEROBEYINN_LOCK_DIR" 2>/dev/null; do
  SEROBEYINN_LOCK_ATTEMPT=$((SEROBEYINN_LOCK_ATTEMPT + 1))
  [ "$SEROBEYINN_LOCK_ATTEMPT" -lt 500 ] || exit 0
  sleep 0.01 2>/dev/null || sleep 1 2>/dev/null || exit 0
done
trap 'rmdir "$SEROBEYINN_LOCK_DIR" 2>/dev/null || :' EXIT
trap 'exit 0' HUP INT TERM

SEROBEYINN_COUNT=0
if [ -f "$SEROBEYINN_PROMPT_COUNT_FILE" ]; then
  SEROBEYINN_COUNT=$(sed -n '1p' "$SEROBEYINN_PROMPT_COUNT_FILE" 2>/dev/null || :)
fi
case "$SEROBEYINN_COUNT" in
  ''|*[!0-9]*) SEROBEYINN_COUNT=0 ;;
esac

SEROBEYINN_COUNT=$((SEROBEYINN_COUNT + 1))
SEROBEYINN_COUNT_TMP="$SEROBEYINN_PROMPT_COUNT_FILE.tmp.$$"
if printf '%s\n' "$SEROBEYINN_COUNT" > "$SEROBEYINN_COUNT_TMP" 2>/dev/null; then
  mv -f "$SEROBEYINN_COUNT_TMP" "$SEROBEYINN_PROMPT_COUNT_FILE" 2>/dev/null || :
fi
rm -f "$SEROBEYINN_COUNT_TMP" 2>/dev/null || :
rmdir "$SEROBEYINN_LOCK_DIR" 2>/dev/null || :
trap - EXIT HUP INT TERM

if [ $((SEROBEYINN_COUNT % 15)) -eq 0 ]; then
  serobeyinn_emit UserPromptSubmit "[Hafıza] $SEROBEYINN_COUNT. mesaj. Oturum sonunda 🔮 850-Companion/Last-Session.md ve Threads.md güncellemeyi unutma."
fi
exit 0
