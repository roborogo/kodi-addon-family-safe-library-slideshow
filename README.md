# Family-Safe Library Slideshow

<div align="center">
  <img src="family-safe-library-slideshow.png" alt="Family-Safe Library Slideshow logo" width="50%">
</div>

A cinematic Kodi screensaver that turns your Movies and TV Shows library artwork into a family-safe slideshow. It pulls fanart and posters directly from the Kodi database and filters images by MPAA/TV ratings so you can safely display content in shared spaces.

## Version
Current version: 1.0.1
Versioning: patch for fixes, minor for new features, major for breaking changes.

## Features
- Smart rating filters for movies (G, PG, PG-13, R, NC-17) and TV shows (TV-Y through TV-MA)
- Optional protection to hide unrated or missing ratings
- Randomized fanart/poster slideshow with smooth crossfades
- Uses Kodi JSON-RPC for fast, library-native artwork access

## Requirements
- Kodi 19+ (Matrix) or newer

## Install (Sideload for testing)
These steps install the addon from a local ZIP or folder without a repository.

### Option A: ZIP install (recommended)
1. From this repo root, create a ZIP of the addon folder contents:
   ```bash
   cd /mnt/c/Users/rogen/github/kodi-addon-family-safe-library-slideshow
   zip -r screensaver.family.safe.library.slideshow.zip addon.py addon.xml icon.png fanart.png resources
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
- Show fanart / posters
- Display time
- Refresh interval
- Enable debug logging (writes extra info to `kodi.log`)
- Allowed rating toggles
- Hide unrated or missing ratings

## What's New
### 1.0.1
- Added a debug logging toggle to help troubleshoot greyed-out menu items.
- Updated metadata to use the new logo.
- Added README versioning and changelog guidance.

## Changelog
### 1.0.1
- Added debug logging setting and runtime logs for library refresh.
- Updated addon icon to `family-safe-library-slideshow.png`.
- Added version section, What's New, and changelog.

### 1.0.0
- Initial release with family-safe rating filters and slideshow.

## Notes
- If no images appear, relax the rating filters or allow unrated content.
- Artwork availability depends on your library having fanart/poster entries.

## Kodi log location
- Windows: `%APPDATA%\\Kodi\\kodi.log`
- Linux: `~/.kodi/temp/kodi.log`
- macOS: `~/Library/Logs/kodi.log`

## License
MIT
