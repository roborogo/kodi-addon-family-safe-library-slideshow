#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ADDON_ID="screensaver.family.safe.library.slideshow"
ZIP_NAME="${ADDON_ID}.zip"

cd "${ROOT_DIR}"

zip -r "${ZIP_NAME}" addon.py addon.xml family-safe-library-slideshow.png fanart.png resources LICENSE README.md

echo "Created ${ZIP_NAME}"
