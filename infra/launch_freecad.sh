#!/usr/bin/env bash
set -euo pipefail
: "${CAD_REQUEST:?}"
: "${CAD_OUTPUT:?}"
mkdir -p "$CAD_OUTPUT"
APP="$PWD/.cache/freecad/1.1.4/squashfs-root/AppRun"
export QTWEBENGINE_DISABLE_SANDBOX=1 LIBGL_ALWAYS_SOFTWARE=1
set +e
timeout --signal=TERM --kill-after=10s 900s xvfb-run -a -s '-screen 0 1600x900x24' "$APP" "$PWD/infra/freecad_worker.py" > "$CAD_OUTPUT/console.log" 2>&1
exit_code=$?
set -e
if [[ ! -f "$CAD_OUTPUT/status.json" ]]; then
  printf '{"success":false,"reason":"FreeCAD no produjo resultado","exit_code":%d}\n' "$exit_code" > "$CAD_OUTPUT/status.json"
fi
python3 - "$CAD_OUTPUT/status.json" <<'PY'
import json,sys
data=json.load(open(sys.argv[1]))
print(data)
if not data.get("success"):sys.exit(1)
PY
