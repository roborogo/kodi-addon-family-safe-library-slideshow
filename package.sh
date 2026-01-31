#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ADDON_ID="screensaver.family.safe.library.slideshow"
ZIP_NAME="${ADDON_ID}.zip"

cd "${ROOT_DIR}"

TMP_DIR=$(mktemp -d)
ADDON_DIR="${TMP_DIR}/${ADDON_ID}"

mkdir -p "${ADDON_DIR}"
cp -R addon.py addon.xml family-safe-library-slideshow.png fanart.png resources LICENSE README.md "${ADDON_DIR}"

cd "${TMP_DIR}"
zip -r "${ZIP_NAME}" "${ADDON_ID}"
mv "${ZIP_NAME}" "${ROOT_DIR}/"
cd "${ROOT_DIR}"
rm -rf "${TMP_DIR}"

echo "Created ${ZIP_NAME}"
