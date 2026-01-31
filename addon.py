# -*- coding: utf-8 -*-
import json
import random
import re
import threading
import time

import xbmc
import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")

MOVIE_RATINGS = ["G", "PG", "PG-13", "R", "NC-17"]
TV_RATINGS = ["TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA"]
UNRATED_TOKENS = ["UNRATED", "NOT RATED", "NOTRATED", "NR", "N R"]


def _debug_enabled():
    try:
        return ADDON.getSettingBool("debug_logging")
    except Exception:
        return ADDON.getSetting("debug_logging").lower() == "true"


def _log(message, level=xbmc.LOGINFO):
    if level >= xbmc.LOGWARNING or _debug_enabled():
        xbmc.log("[FamilySafeSlideshow] {}".format(message), level)


def _get_setting_bool(key, default=False):
    try:
        return ADDON.getSettingBool(key)
    except Exception:
        value = ADDON.getSetting(key)
        if value == "":
            return default
        return value.lower() == "true"


def _get_setting_int(key, default=0):
    try:
        return ADDON.getSettingInt(key)
    except Exception:
        value = ADDON.getSetting(key)
        if value == "":
            return default
        try:
            return int(value)
        except ValueError:
            return default


def _json_rpc(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }
    response = xbmc.executeJSONRPC(json.dumps(payload))
    try:
        data = json.loads(response)
    except ValueError:
        _log("Invalid JSON-RPC response for {}".format(method), xbmc.LOGWARNING)
        return {}
    return data.get("result", {})


def _normalize_key(value):
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def _extract_rating(raw_text, allowed_keys):
    if not raw_text:
        return None
    text = raw_text.upper().strip()
    if any(token in text for token in UNRATED_TOKENS):
        return None
    text = re.sub(r"\bRATED\b", "", text).strip()
    for key in allowed_keys:
        if key in text:
            return key
    normalized = _normalize_key(text)
    normalized_map = {_normalize_key(key): key for key in allowed_keys}
    return normalized_map.get(normalized)


def _rating_allowed(raw_text, allowed_map, hide_unrated):
    rating = _extract_rating(raw_text, list(allowed_map.keys()))
    if rating is None:
        return not hide_unrated
    return allowed_map.get(rating, False)


def _resolve_image_path(image_path):
    if not image_path:
        return None
    if image_path.startswith("special://"):
        return xbmc.translatePath(image_path)
    return image_path


class Settings(object):
    def __init__(self):
        self.reload()

    def reload(self):
        self.include_movies = _get_setting_bool("include_movies", True)
        self.include_tvshows = _get_setting_bool("include_tvshows", True)
        self.show_fanart = _get_setting_bool("show_fanart", True)
        self.show_posters = _get_setting_bool("show_posters", True)
        self.display_seconds = max(5, _get_setting_int("display_seconds", 10))
        self.refresh_minutes = max(1, _get_setting_int("refresh_minutes", 10))
        self.hide_unrated = _get_setting_bool("hide_unrated", True)

        self.allowed_movies = {
            "G": _get_setting_bool("movie_rating_g", True),
            "PG": _get_setting_bool("movie_rating_pg", True),
            "PG-13": _get_setting_bool("movie_rating_pg13", True),
            "R": _get_setting_bool("movie_rating_r", False),
            "NC-17": _get_setting_bool("movie_rating_nc17", False),
        }
        self.allowed_tv = {
            "TV-Y": _get_setting_bool("tv_rating_tvy", True),
            "TV-Y7": _get_setting_bool("tv_rating_tvy7", True),
            "TV-G": _get_setting_bool("tv_rating_tvg", True),
            "TV-PG": _get_setting_bool("tv_rating_tvpg", True),
            "TV-14": _get_setting_bool("tv_rating_tv14", True),
            "TV-MA": _get_setting_bool("tv_rating_tvma", False),
        }


class SlideshowWindow(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        super(SlideshowWindow, self).__init__(*args, **kwargs)
        self._monitor = xbmc.Monitor()
        self._settings = Settings()
        self._images = []
        self._last_refresh = 0
        self._front = None
        self._back = None
        self._front_visible = True
        self._running = True

    def onInit(self):
        self._front = self.getControl(100)
        self._back = self.getControl(101)
        self._front.setVisible(True)
        self._back.setVisible(False)
        threading.Thread(target=self._run, daemon=True).start()

    def onAction(self, action):
        if action.getId() in (
            xbmcgui.ACTION_PREVIOUS_MENU,
            xbmcgui.ACTION_NAV_BACK,
            xbmcgui.ACTION_STOP,
        ):
            self._running = False
            self.close()

    def _run(self):
        self._reload_images(force=True)
        index = 0
        while self._running and not self._monitor.abortRequested():
            if not self._images:
                if self._monitor.waitForAbort(1.0):
                    break
                self._reload_images()
                continue

            image = self._images[index % len(self._images)]
            self._show_image(image)
            index += 1

            if self._wait_with_abort(self._settings.display_seconds):
                break

            if time.time() - self._last_refresh >= self._settings.refresh_minutes * 60:
                self._reload_images(force=True)
                index = 0

        self.close()

    def _wait_with_abort(self, seconds):
        end_time = time.time() + seconds
        while time.time() < end_time:
            if self._monitor.waitForAbort(0.2):
                return True
        return False

    def _reload_images(self, force=False):
        now = time.time()
        if not force and now - self._last_refresh < self._settings.refresh_minutes * 60:
            return
        self._settings.reload()
        _log("Reloading library images (force={})".format(force))
        self._last_refresh = now
        self._images = self._fetch_images()
        if not self._images:
            _log("No images found after filtering; check ratings or artwork availability.", xbmc.LOGWARNING)

    def _fetch_images(self):
        images = []
        seen = set()

        if self._settings.include_movies:
            movies = _json_rpc(
                "VideoLibrary.GetMovies",
                {"properties": ["art", "mpaa"]},
            ).get("movies", [])
            _log("Movies fetched: {}".format(len(movies)))
            images.extend(self._collect_images(movies, self._settings.allowed_movies))

        if self._settings.include_tvshows:
            shows = _json_rpc(
                "VideoLibrary.GetTVShows",
                {"properties": ["art", "mpaa"]},
            ).get("tvshows", [])
            _log("TV shows fetched: {}".format(len(shows)))
            images.extend(self._collect_images(shows, self._settings.allowed_tv))

        unique_images = []
        for image in images:
            if image not in seen:
                seen.add(image)
                unique_images.append(image)

        random.shuffle(unique_images)
        _log("Images available after filtering: {}".format(len(unique_images)))
        return unique_images

    def _collect_images(self, items, allowed_ratings):
        collected = []
        for item in items or []:
            if not _rating_allowed(item.get("mpaa"), allowed_ratings, self._settings.hide_unrated):
                continue
            art = item.get("art") or {}
            if self._settings.show_fanart:
                fanart = _resolve_image_path(art.get("fanart"))
                if fanart:
                    collected.append(fanart)
            if self._settings.show_posters:
                poster = _resolve_image_path(art.get("poster"))
                if poster:
                    collected.append(poster)
        return collected

    def _show_image(self, image):
        if not self._front or not self._back:
            return
        if self._front_visible:
            self._back.setImage(image)
            self._back.setVisible(True)
            self._front.setVisible(False)
        else:
            self._front.setImage(image)
            self._front.setVisible(True)
            self._back.setVisible(False)
        self._front_visible = not self._front_visible


def run():
    _log("Starting screensaver window")
    window = SlideshowWindow("Slideshow.xml", ADDON_PATH, "default", "1080i")
    window.doModal()
    del window


if __name__ == "__main__":
    run()
