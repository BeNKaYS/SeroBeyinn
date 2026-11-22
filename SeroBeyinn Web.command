#!/bin/sh
# SeroBeyinn Web arayuzunu acar. Kurulu vault uzerinden calisir; token girmene gerek kalmaz.
VAULT="/Users/benkays/Documents/SeroBeyinn"
if [ ! -f "$VAULT/serobeyinn.py" ]; then
  echo "Kurulu SeroBeyinn vault bulunamadi: $VAULT"
  echo "Once SETUP.md adimlarini izleyip kurulumu tamamla."
  printf "\nKapatmak icin Enter. "
  read -r _
  exit 1
fi
cd "$VAULT" || exit 1
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
exec "$PY" serobeyinn.py web ac
