$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$addonId = 'screensaver.family.safe.library.slideshow'
$zipName = "$addonId.zip"

Set-Location $root

$items = @(
  'addon.py',
  'addon.xml',
  'family-safe-library-slideshow.png',
  'fanart.png',
  'resources',
  'LICENSE',
  'README.md'
)

if (Test-Path $zipName) {
  Remove-Item $zipName -Force
}

Compress-Archive -Path $items -DestinationPath $zipName
Write-Host "Created $zipName"
