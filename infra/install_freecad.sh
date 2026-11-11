#!/usr/bin/env bash
set -euo pipefail
VERSION=1.1.4
FILE="FreeCAD_${VERSION}-Linux-x86_64-py311.AppImage"
SHA256="f6dc6ba676e5ac96a565ebc8d657232f94c6158e85b4352141bd1a46f6b43434"
URL="https://github.com/FreeCAD/FreeCAD/releases/download/${VERSION}/${FILE}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CACHE="$ROOT/.cache/freecad/${VERSION}"
mkdir -p "$CACHE"
if [[ ! -f "$CACHE/squashfs-root/AppRun" ]]; then
  if [[ ! -f "$CACHE/$FILE" ]]; then
    curl --fail --location --retry 3 --retry-all-errors --connect-timeout 30 --output "$CACHE/$FILE" "$URL"
  fi
  (cd "$CACHE"; echo "$SHA256  $FILE" | sha256sum --check)
  chmod +x "$CACHE/$FILE"
  (cd "$CACHE"; "./$FILE" --appimage-extract >/dev/null)
fi
chmod +x "$CACHE/squashfs-root/AppRun"
echo "FreeCAD preparado en caché"
