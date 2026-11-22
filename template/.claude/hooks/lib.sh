#!/bin/bash
[ -n "${SEROBEYINN_INVOKED_BY:-}" ] && exit 0
# Shared, portable helpers for all SeroBeyinn hooks.

if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
  SEROBEYINN_PROJECT_DIR=$CLAUDE_PROJECT_DIR
else
  SEROBEYINN_HOOK_DIR=$(CDPATH= cd "$(dirname "$0")" 2>/dev/null && pwd)
  SEROBEYINN_PROJECT_DIR=$(CDPATH= cd "$SEROBEYINN_HOOK_DIR/../.." 2>/dev/null && pwd)
fi

SEROBEYINN_STATE_DIR="$SEROBEYINN_PROJECT_DIR/.claude/scripts/.state"
mkdir -p "$SEROBEYINN_STATE_DIR" 2>/dev/null || :

serobeyinn_mark_python_missing() {
  mkdir -p "$SEROBEYINN_STATE_DIR" 2>/dev/null || :
  : > "$SEROBEYINN_STATE_DIR/python3-missing" 2>/dev/null || :
}

serobeyinn_mtime() {
  SEROBEYINN_MTIME_VALUE=""
  if [ -f "$1" ]; then
    SEROBEYINN_MTIME_VALUE=$(stat -f %m "$1" 2>/dev/null || :)
    case "$SEROBEYINN_MTIME_VALUE" in
      ''|*[!0-9]*)
        SEROBEYINN_MTIME_VALUE=$(stat -c %Y "$1" 2>/dev/null || :)
        ;;
    esac
  fi

  case "$SEROBEYINN_MTIME_VALUE" in
    ''|*[!0-9]*) printf '%s\n' 0 ;;
    *) printf '%s\n' "$SEROBEYINN_MTIME_VALUE" ;;
  esac
}

serobeyinn_json_escape() {
  if ! command -v python3 >/dev/null 2>&1; then
    serobeyinn_mark_python_missing
    return 1
  fi

  if ! python3 -c 'import json, sys; print(json.dumps(sys.stdin.read()))'; then
    serobeyinn_mark_python_missing
    return 1
  fi
}

serobeyinn_session_key() {
  if ! command -v python3 >/dev/null 2>&1; then
    serobeyinn_mark_python_missing
    return 1
  fi

  python3 -c '
import hashlib
import json
import sys

payload = json.load(sys.stdin)
session_id = payload.get("session_id") if isinstance(payload, dict) else None
if not isinstance(session_id, str) or not session_id:
    raise SystemExit(1)
print(hashlib.sha256(session_id.encode("utf-8")).hexdigest())
' 2>/dev/null
}

serobeyinn_cleanup_session_state() {
  [ -d "$SEROBEYINN_STATE_DIR" ] || return 0

  find "$SEROBEYINN_STATE_DIR" -type f \( \
    -name 'session_start_time.*' -o \
    -name 'prompt_count.*' -o \
    -name 'needs_reflection.*' -o \
    -name 'hookin-*.json' \
  \) -mtime +7 -exec rm -f {} \; 2>/dev/null || :
  find "$SEROBEYINN_STATE_DIR" -type d -name 'prompt_count.*.lock' \
    -mtime +7 -exec rmdir {} \; 2>/dev/null || :
}

serobeyinn_emit() {
  SEROBEYINN_EVENT=$1
  SEROBEYINN_TEXT=$2

  case "$SEROBEYINN_EVENT" in
    SessionStart|UserPromptSubmit|SessionEnd|PreCompact) ;;
    *) return 0 ;;
  esac

  SEROBEYINN_ESCAPED=$(printf '%s' "$SEROBEYINN_TEXT" | serobeyinn_json_escape 2>/dev/null || :)
  if [ -n "$SEROBEYINN_ESCAPED" ]; then
    printf '{"hookSpecificOutput":{"hookEventName":"%s","additionalContext":%s}}\n' \
      "$SEROBEYINN_EVENT" "$SEROBEYINN_ESCAPED"
    return 0
  fi

  serobeyinn_mark_python_missing
  SEROBEYINN_FALLBACK='SeroBeyinn uyarisi: python3 bulunamadi. serobeyinn-doktor calistir.'
  SEROBEYINN_FALLBACK=$(printf '%s' "$SEROBEYINN_FALLBACK" | sed 's/\\/\\\\/g; s/"/\\"/g' 2>/dev/null || :)
  [ -n "$SEROBEYINN_FALLBACK" ] || return 0
  printf '{"hookSpecificOutput":{"hookEventName":"%s","additionalContext":"%s"}}\n' \
    "$SEROBEYINN_EVENT" "$SEROBEYINN_FALLBACK"
}

serobeyinn_yesterday() {
  SEROBEYINN_YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || :)
  if [ -z "$SEROBEYINN_YESTERDAY" ]; then
    SEROBEYINN_YESTERDAY=$(date -d yesterday '+%Y-%m-%d' 2>/dev/null || :)
  fi
  printf '%s\n' "$SEROBEYINN_YESTERDAY"
}
