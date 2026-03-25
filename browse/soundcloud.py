#!/usr/bin/env python3
import os
import time
import logging
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_set(path):
    if os.path.exists(path):
        with open(path) as f:
            return set(x.strip() for x in f if x.strip())
    return set()


def append_lines(path, lines):
    with open(path, "a") as f:
        for line in lines:
            f.write(line + "\n")


def extract_entries(url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    entries = info.get("entries", [])
    urls = []

    for e in entries:
        if not e:
            continue
        webpage_url = e.get("url") or e.get("webpage_url")
        if webpage_url:
            urls.append(webpage_url)

    return urls


def likes_url(username: str) -> str:
    return f"https://soundcloud.com/{username}/likes"


def playlist_url(username: str, set_name: str, is_user_playlist: bool = False) -> str:
    if is_user_playlist:
        return f"https://soundcloud.com/{username}/sets/{set_name}"
    return f"https://soundcloud.com/{username}/sets/{set_name}"


def extract_likes(username: str):
    return extract_entries(likes_url(username))


def extract_playlist(username: str, set_name: str, is_user_playlist: bool = False):
    return extract_entries(playlist_url(username, set_name, is_user_playlist))


def download_urls(urls):
    downloaded = load_set("downloaded.txt")
    ignored = load_set("ignored.txt")
    seen = downloaded | ignored

    urls = [u for u in urls if u not in seen]

    if not urls:
        logger.info("No new tracks")
        return

    os.makedirs("songs", exist_ok=True)

    ydl_opts = {
        "outtmpl": "songs/%(uploader)s - %(title)s (%(id)s).%(ext)s",
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    success = []
    failed = []

    with YoutubeDL(ydl_opts) as ydl:
        for i, url in enumerate(urls, 1):
            logger.info(f"{i}/{len(urls)} downloading")
            try:
                ydl.download([url])
                success.append(url)
            except Exception as e:
                failed.append((url, str(e)))
            time.sleep(1)

    append_lines("downloaded.txt", success)

    if failed:
        with open("errors.txt", "a") as f:
            f.write(f"\n\nRun @ {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for url, err in failed:
                f.write(f"{url}\n{err}\n\n")


def run_likes(username: str):
    logger.info(f"Fetching likes for: {username}")
    urls = extract_likes(username)
    download_urls(urls)

def run_playlist(username: str, set_name: str, is_user_playlist: bool = False):
    logger.info(f"Fetching playlist: {username} / {set_name}")
    urls = extract_playlist(username, set_name, is_user_playlist)
    download_urls(urls)
