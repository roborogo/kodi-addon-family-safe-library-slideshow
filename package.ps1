param(
  [switch]$Pause
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$addonId = 'screensaver.family.safe.library.slideshow'
$zipName = "$addonId.zip"

Set-Location $root

if (Test-Path $zipName) {
  Remove-Item $zipName -Force
}

$tempDir = Join-Path $env:TEMP ([guid]::NewGuid().ToString())
$addonDir = Join-Path $tempDir $addonId
New-Item -ItemType Directory -Path $addonDir | Out-Null

$items = @(
  'addon.py',
  'addon.xml',
  'icon.png',
  'fanart.png',
  'resources',
  'LICENSE',
  'README.md'
)

foreach ($item in $items) {
  Copy-Item -Path (Join-Path $root $item) -Destination $addonDir -Recurse -Force
}

try {
  Compress-Archive -Path $addonDir -DestinationPath (Join-Path $root $zipName)
  Remove-Item $tempDir -Recurse -Force
  Write-Host "Created $zipName"
} catch {
  Write-Error $_
  if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
  }
  if (-not $Pause) {
    $Pause = $true
  }
}

if ($Pause) {
  Read-Host "Press Enter to exit"
}
