#!/bin/sh
# SeroBeyinn Web arayuzunu acar. Kurulu vault uzerinden calisir; token girmene gerek kalmaz.
VAULT="/Users/benkays/Documents/SeroBeyinn"
REPO="/Users/benkays/Desktop/Dev_Folder/SeroBeyinn/template/.claude/scripts"
if [ ! -f "$VAULT/serobeyinn.py" ]; then
  echo "Kurulu SeroBeyinn vault bulunamadi: $VAULT"
  echo "Once SETUP.md adimlarini izleyip kurulumu tamamla."
  printf "\nKapatmak icin Enter. "
  read -r _
  exit 1
fi
PY=""
for candidate in python3.15 python3.14 python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then PY="$candidate"; break; fi
done
if [ -z "$PY" ]; then
  echo "Python 3.11+ bulunamadi."
  printf "\nKapatmak icin Enter. "
  read -r _
  exit 1
fi
cd "$VAULT" || exit 1
CHANGED=0
for f in serobeyinn_v3_web.py serobeyinn_v3_web_ui.py; do
  if [ -f "$REPO/$f" ] && ! cmp -s "$REPO/$f" "$VAULT/.claude/scripts/$f"; then
    cp "$REPO/$f" "$VAULT/.claude/scripts/$f" && CHANGED=1
  fi
done
if [ "$CHANGED" = "1" ]; then
  "$PY" serobeyinn.py web durdur >/dev/null 2>&1 || true
fi
exec "$PY" serobeyinn.py web ac
