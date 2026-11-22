#!/bin/bash
[ -n "${SEROBEYINN_INVOKED_BY:-}" ] && exit 0
# Inject relational memory, rules, recent journal context, and the knowledge index.

SEROBEYINN_HOOK_DIR=$(CDPATH= cd "$(dirname "$0")" 2>/dev/null && pwd)
. "$SEROBEYINN_HOOK_DIR/lib.sh" 2>/dev/null || exit 0

SEROBEYINN_MEMORY_DIR="$SEROBEYINN_PROJECT_DIR/🔮 850-Companion"
mkdir -p "$SEROBEYINN_STATE_DIR" 2>/dev/null || :
serobeyinn_cleanup_session_state

SEROBEYINN_SESSION_KEY=$(serobeyinn_session_key 2>/dev/null || :)
if [ -n "$SEROBEYINN_SESSION_KEY" ]; then
  SEROBEYINN_SESSION_START_FILE="$SEROBEYINN_STATE_DIR/session_start_time.$SEROBEYINN_SESSION_KEY"
  SEROBEYINN_PROMPT_COUNT_FILE="$SEROBEYINN_STATE_DIR/prompt_count.$SEROBEYINN_SESSION_KEY"
  date '+%s' > "$SEROBEYINN_SESSION_START_FILE" 2>/dev/null || :
  printf '%s\n' 0 > "$SEROBEYINN_PROMPT_COUNT_FILE" 2>/dev/null || :
fi

SEROBEYINN_LAST_SESSION=""
if [ -f "$SEROBEYINN_MEMORY_DIR/Last-Session.md" ]; then
  SEROBEYINN_LAST_SESSION=$(awk '
    /^## Session:/ { active = 1 }
    active && /^## Previous/ { exit }
    active { print }
  ' "$SEROBEYINN_MEMORY_DIR/Last-Session.md" 2>/dev/null | sed -n '1,50p')
fi

SEROBEYINN_THREADS=""
if [ -f "$SEROBEYINN_MEMORY_DIR/Threads.md" ]; then
  SEROBEYINN_THREADS=$(sed -n '/^## Active/,/^## Closed/p' "$SEROBEYINN_MEMORY_DIR/Threads.md" 2>/dev/null \
    | grep -E '^### |^\*\*Status:\*\*' 2>/dev/null \
    | sed -n '1,12p')
fi

SEROBEYINN_RULES=""
if [ -f "$SEROBEYINN_MEMORY_DIR/Kurallar.md" ]; then
  SEROBEYINN_RULES=$(sed -n '1,60p' "$SEROBEYINN_MEMORY_DIR/Kurallar.md" 2>/dev/null)
fi

SEROBEYINN_JOURNAL=""
if [ -f "$SEROBEYINN_MEMORY_DIR/Journal.md" ]; then
  SEROBEYINN_JOURNAL_LINE=$(grep -n '^## ' "$SEROBEYINN_MEMORY_DIR/Journal.md" 2>/dev/null \
    | tail -n 1 | cut -d: -f1)
  case "$SEROBEYINN_JOURNAL_LINE" in
    ''|*[!0-9]*) ;;
    *)
      SEROBEYINN_JOURNAL_END=$((SEROBEYINN_JOURNAL_LINE + 9))
      SEROBEYINN_JOURNAL=$(sed -n "${SEROBEYINN_JOURNAL_LINE},${SEROBEYINN_JOURNAL_END}p" \
        "$SEROBEYINN_MEMORY_DIR/Journal.md" 2>/dev/null)
      ;;
  esac
fi

SEROBEYINN_INDEX=""
if [ -f "$SEROBEYINN_PROJECT_DIR/knowledge/index.md" ]; then
  SEROBEYINN_INDEX=$(sed -n '1,150p' "$SEROBEYINN_PROJECT_DIR/knowledge/index.md" 2>/dev/null)
fi

SEROBEYINN_DAILY=""
SEROBEYINN_TODAY=$(date '+%Y-%m-%d' 2>/dev/null || :)
SEROBEYINN_DAILY_FILE=""
if [ -n "$SEROBEYINN_TODAY" ] && [ -f "$SEROBEYINN_PROJECT_DIR/daily/$SEROBEYINN_TODAY.md" ]; then
  SEROBEYINN_DAILY_FILE="$SEROBEYINN_PROJECT_DIR/daily/$SEROBEYINN_TODAY.md"
else
  SEROBEYINN_YESTERDAY=$(serobeyinn_yesterday)
  if [ -n "$SEROBEYINN_YESTERDAY" ] && [ -f "$SEROBEYINN_PROJECT_DIR/daily/$SEROBEYINN_YESTERDAY.md" ]; then
    SEROBEYINN_DAILY_FILE="$SEROBEYINN_PROJECT_DIR/daily/$SEROBEYINN_YESTERDAY.md"
  fi
fi
[ -n "$SEROBEYINN_DAILY_FILE" ] && SEROBEYINN_DAILY=$(tail -n 25 "$SEROBEYINN_DAILY_FILE" 2>/dev/null)

SEROBEYINN_NL='
'
SEROBEYINN_REFLECTION=""
for SEROBEYINN_REFLECTION_FILE in \
  "$SEROBEYINN_STATE_DIR/needs_reflection" \
  "$SEROBEYINN_STATE_DIR"/needs_reflection.*
do
  [ -f "$SEROBEYINN_REFLECTION_FILE" ] || continue
  SEROBEYINN_REFLECTION_DETAIL=$(sed -n '1p' "$SEROBEYINN_REFLECTION_FILE" 2>/dev/null || :)
  if [ -n "$SEROBEYINN_REFLECTION_DETAIL" ]; then
    [ -n "$SEROBEYINN_REFLECTION" ] && SEROBEYINN_REFLECTION="${SEROBEYINN_REFLECTION}${SEROBEYINN_NL}"
    SEROBEYINN_REFLECTION="${SEROBEYINN_REFLECTION}⚠️ Önceki oturum hafıza güncellemeden bitti: ${SEROBEYINN_REFLECTION_DETAIL}. Anlamlı bir şey olduysa 🔮 850-Companion dosyalarını güncelle."
  fi
  rm -f "$SEROBEYINN_REFLECTION_FILE" 2>/dev/null || :
done

# Hard section entry caps, including truncation notes: Last Session 4000,
# Threads 2000, Kurallar 4000, Journal 1500, reflection debt 1000 characters.
serobeyinn_cap_section() {
  SEROBEYINN_CAP_VALUE=$1
  SEROBEYINN_CAP_LIMIT=$2
  SEROBEYINN_CAP_NOTE=$3
  if [ "${#SEROBEYINN_CAP_VALUE}" -le "$SEROBEYINN_CAP_LIMIT" ]; then
    printf '%s' "$SEROBEYINN_CAP_VALUE"
    return 0
  fi

  SEROBEYINN_CAP_KEEP=$((SEROBEYINN_CAP_LIMIT - ${#SEROBEYINN_CAP_NOTE} - 1))
  [ "$SEROBEYINN_CAP_KEEP" -gt 0 ] || SEROBEYINN_CAP_KEEP=0
  printf '%s\n%s' "${SEROBEYINN_CAP_VALUE:0:$SEROBEYINN_CAP_KEEP}" "$SEROBEYINN_CAP_NOTE"
}

SEROBEYINN_LAST_SESSION=$(serobeyinn_cap_section "$SEROBEYINN_LAST_SESSION" 4000 \
  '[not: son oturum 4.000 karakterde kırpıldı, serobeyinn-doktor çalıştır]')
SEROBEYINN_THREADS=$(serobeyinn_cap_section "$SEROBEYINN_THREADS" 2000 \
  '[not: aktif konular 2.000 karakterde kırpıldı, serobeyinn-doktor çalıştır]')
SEROBEYINN_RULES=$(serobeyinn_cap_section "$SEROBEYINN_RULES" 4000 \
  '[not: kurallar 4.000 karakterde kırpıldı, serobeyinn-doktor çalıştır]')
SEROBEYINN_JOURNAL=$(serobeyinn_cap_section "$SEROBEYINN_JOURNAL" 1500 \
  '[not: son Journal 1.500 karakterde kırpıldı, serobeyinn-doktor çalıştır]')
SEROBEYINN_REFLECTION=$(serobeyinn_cap_section "$SEROBEYINN_REFLECTION" 1000 \
  '[not: hafıza uyarıları 1.000 karakterde kırpıldı, serobeyinn-doktor çalıştır]')

SEROBEYINN_TRUNCATED=0
SEROBEYINN_CLOSING='[Hafıza] Süreklilik senin sorumluluğun. Bu kullanıcı için kim olduğunu anlamak üzere 🔮 850-Companion/Core.md dosyasını oku.
Hafıza protokolü zorunludur.'
SEROBEYINN_TRUNCATION_NOTE='[not: indeks kırpıldı, serobeyinn-doktor çalıştır]'
SEROBEYINN_CAP_DIAGNOSTIC='SeroBeyinn uyarısı: Oturum başlangıç bağlamı 16.000 karakter sınırına sığmadı. Bölüm limitlerini kontrol etmek için serobeyinn-doktor çalıştır.'

serobeyinn_build_context() {
  SEROBEYINN_CONTEXT=""
  [ -n "$SEROBEYINN_REFLECTION" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}${SEROBEYINN_REFLECTION}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ -n "$SEROBEYINN_LAST_SESSION" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}[Hafıza: Son Oturum]${SEROBEYINN_NL}${SEROBEYINN_LAST_SESSION}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ -n "$SEROBEYINN_THREADS" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}[Hafıza: Aktif Konular]${SEROBEYINN_NL}${SEROBEYINN_THREADS}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ -n "$SEROBEYINN_RULES" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}[Hafıza: Kurallar]${SEROBEYINN_NL}${SEROBEYINN_RULES}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ -n "$SEROBEYINN_JOURNAL" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}[Hafıza: Son Journal]${SEROBEYINN_NL}${SEROBEYINN_JOURNAL}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ -n "$SEROBEYINN_INDEX" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}[Bilgi Tabanı: İndeks]${SEROBEYINN_NL}${SEROBEYINN_INDEX}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ -n "$SEROBEYINN_DAILY" ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}[Bugünün Logu]${SEROBEYINN_NL}${SEROBEYINN_DAILY}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  [ "$SEROBEYINN_TRUNCATED" -eq 1 ] && SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}${SEROBEYINN_TRUNCATION_NOTE}${SEROBEYINN_NL}${SEROBEYINN_NL}"
  SEROBEYINN_CONTEXT="${SEROBEYINN_CONTEXT}${SEROBEYINN_CLOSING}"
}

serobeyinn_build_context
if [ "${#SEROBEYINN_CONTEXT}" -gt 16000 ]; then
  SEROBEYINN_TRUNCATED=1
  serobeyinn_build_context

  SEROBEYINN_OVER=$(( ${#SEROBEYINN_CONTEXT} - 16000 ))
  if [ "$SEROBEYINN_OVER" -gt 0 ] && [ -n "$SEROBEYINN_INDEX" ]; then
    if [ "$SEROBEYINN_OVER" -ge "${#SEROBEYINN_INDEX}" ]; then
      SEROBEYINN_INDEX=""
    else
      SEROBEYINN_KEEP=$(( ${#SEROBEYINN_INDEX} - SEROBEYINN_OVER ))
      SEROBEYINN_INDEX=${SEROBEYINN_INDEX:0:$SEROBEYINN_KEEP}
    fi
    serobeyinn_build_context
  fi

  SEROBEYINN_OVER=$(( ${#SEROBEYINN_CONTEXT} - 16000 ))
  if [ "$SEROBEYINN_OVER" -gt 0 ] && [ -n "$SEROBEYINN_DAILY" ]; then
    if [ "$SEROBEYINN_OVER" -ge "${#SEROBEYINN_DAILY}" ]; then
      SEROBEYINN_DAILY=""
    else
      SEROBEYINN_DAILY=${SEROBEYINN_DAILY:$SEROBEYINN_OVER}
    fi
    serobeyinn_build_context
  fi

  # Journal and reflection are the only remaining non-protected sections.
  SEROBEYINN_OVER=$(( ${#SEROBEYINN_CONTEXT} - 16000 ))
  if [ "$SEROBEYINN_OVER" -gt 0 ] && [ -n "$SEROBEYINN_JOURNAL" ]; then
    if [ "$SEROBEYINN_OVER" -ge "${#SEROBEYINN_JOURNAL}" ]; then
      SEROBEYINN_JOURNAL=""
    else
      SEROBEYINN_KEEP=$(( ${#SEROBEYINN_JOURNAL} - SEROBEYINN_OVER ))
      SEROBEYINN_JOURNAL=${SEROBEYINN_JOURNAL:0:$SEROBEYINN_KEEP}
    fi
    serobeyinn_build_context
  fi

  SEROBEYINN_OVER=$(( ${#SEROBEYINN_CONTEXT} - 16000 ))
  if [ "$SEROBEYINN_OVER" -gt 0 ] && [ -n "$SEROBEYINN_REFLECTION" ]; then
    if [ "$SEROBEYINN_OVER" -ge "${#SEROBEYINN_REFLECTION}" ]; then
      SEROBEYINN_REFLECTION=""
    else
      SEROBEYINN_KEEP=$(( ${#SEROBEYINN_REFLECTION} - SEROBEYINN_OVER ))
      SEROBEYINN_REFLECTION=${SEROBEYINN_REFLECTION:0:$SEROBEYINN_KEEP}
    fi
    serobeyinn_build_context
  fi
fi

if [ "${#SEROBEYINN_CONTEXT}" -gt 16000 ]; then
  SEROBEYINN_CONTEXT=$SEROBEYINN_CAP_DIAGNOSTIC
fi

[ -n "$SEROBEYINN_CONTEXT" ] && serobeyinn_emit SessionStart "$SEROBEYINN_CONTEXT"

# The evening compile is triggered from SessionEnd, which means a day whose last
# session closes before 18:00 never reaches it and its log sits uncompiled. Fire
# the catch-up pass here, detached and after the context is already emitted so it
# can neither delay the session nor corrupt the hook's JSON on stdout. flush.py
# decides whether anything is actually due; the call is cheap when it is not.
if command -v python3 >/dev/null 2>&1; then
  nohup python3 "$SEROBEYINN_PROJECT_DIR/.claude/scripts/flush.py" \
    --maybe-compile >/dev/null 2>&1 &
fi

exit 0
