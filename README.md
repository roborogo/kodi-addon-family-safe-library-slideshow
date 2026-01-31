# Family-Safe Library Slideshow

<div align="center">
  <img src="icon.png" alt="Family-Safe Library Slideshow logo" width="50%">
</div>

A cinematic Kodi screensaver that turns your Movies and TV Shows library artwork into a family-safe slideshow. It pulls fanart directly from the Kodi database and filters images by MPAA/TV ratings so you can safely display content in shared spaces.

## Version
Current version: 1.0.9
Versioning: patch for fixes, minor for new features, major for breaking changes.

## Features
- Smart rating filters for movies (G, PG, PG-13, R, NC-17) and TV shows (TV-Y through TV-MA)
- Optional protection to hide unrated or missing ratings
- Randomized fanart slideshow with smooth crossfades
- Uses Kodi JSON-RPC for fast, library-native artwork access

## Requirements
- Kodi 19+ (Matrix) or newer

## Install (Sideload for testing)
These steps install the addon from a local ZIP or folder without a repository.

### Option A: ZIP install (recommended)
1. From this repo root, create a ZIP that contains the addon folder:
   ```bash
   cd /mnt/c/Users/rogen/github/kodi-addon-family-safe-library-slideshow
   ./package.sh
   ```
   On Windows PowerShell, you can run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\package.ps1
   ```
   If you double-click the script, use:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\package.ps1 -Pause
   ```
2. In Kodi, enable Unknown sources:
   - Settings -> System -> Add-ons -> Unknown sources -> On
3. Install from ZIP:
   - Add-ons -> Install from zip file -> select `screensaver.family.safe.library.slideshow.zip`
4. Activate the screensaver:
   - Settings -> Interface -> Screensaver -> Screensaver mode -> Family-Safe Library Slideshow

### Option B: Add-ons folder (dev install)
1. Copy this repo folder into your Kodi addons directory:
   - Windows: `%APPDATA%\Kodi\addons\screensaver.family.safe.library.slideshow`
   - Linux: `~/.kodi/addons/screensaver.family.safe.library.slideshow`
   - macOS: `~/Library/Application Support/Kodi/addons/screensaver.family.safe.library.slideshow`
2. Ensure the folder name matches the addon id:
   - `screensaver.family.safe.library.slideshow`
3. In Kodi, go to Add-ons -> My add-ons -> Screensavers, then enable it.
4. Set it as the active screensaver:
   - Settings -> Interface -> Screensaver -> Screensaver mode -> Family-Safe Library Slideshow

## Configuration
Go to Add-ons -> My add-ons -> Screensavers -> Family-Safe Library Slideshow -> Configure.

Settings include:
- Include movies / TV shows
- Show fanart
- Display time
- Refresh interval
- Enable debug logging (writes extra info to `kodi.log`)
- Allowed rating toggles
- Hide unrated or missing ratings

## What's New
### 1.0.9
- Fixed PowerShell ZIP validation on Windows path separators.

### 1.0.8
- PowerShell packaging now uses .NET zip with validation of `addon.xml` inside the ZIP.

### 1.0.7
- Fixed PowerShell ZIP structure so Kodi can read `addon.xml`.

### 1.0.6
- Fixed packaging scripts to use `icon.png`.

### 1.0.5
- Added icon and fanart assets.

### 1.0.4
- Packaging scripts now create a Kodi-compatible ZIP with the addon folder.

### 1.0.3
- Slideshow now uses fanart only.

### 1.0.2
- Fixed Kodi 21 settings separator type and a shutdown action crash.
- Prevented focus errors in the screensaver window.

### 1.0.1
- Added a debug logging toggle to help troubleshoot greyed-out menu items.
- Updated metadata to use the new logo.
- Added README versioning and changelog guidance.

## Changelog
### 1.0.9
- Normalized ZIP entry paths in `package.ps1` validation.

### 1.0.8
- Rebuilt `package.ps1` to create a validated Kodi-compatible ZIP.

### 1.0.7
- PowerShell packaging now zips the addon folder at the top level.

### 1.0.6
- Packaging scripts now include `icon.png` (not the removed logo file).

### 1.0.5
- Added icon and fanart assets.

### 1.0.4
- Updated packaging scripts and instructions for Kodi ZIP structure.

### 1.0.3
- Removed poster artwork from the slideshow (fanart only).

### 1.0.2
- Fixed settings separator type for Kodi 21 settings UI.
- Removed invalid shutdown action constant.
- Made image controls non-focusable to stop focus warnings.

### 1.0.1
- Added debug logging setting and runtime logs for library refresh.
- Updated addon icon to `family-safe-library-slideshow.png`.
- Added version section, What's New, and changelog.

### 1.0.0
- Initial release with family-safe rating filters and slideshow.

## Notes
- If no images appear, relax the rating filters or allow unrated content.
- Artwork availability depends on your library having fanart entries.

## Kodi log location
- Windows: `%APPDATA%\\Kodi\\kodi.log`
- Linux: `~/.kodi/temp/kodi.log`
- macOS: `~/Library/Logs/kodi.log`

## License
MIT
