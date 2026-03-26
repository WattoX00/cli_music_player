#!/usr/bin/env python3
import time
import logging
from pathlib import Path
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path.home() / "Music"

def load_set(path: Path):
    if path.exists():
        with path.open() as f:
            return set(x.strip() for x in f if x.strip())
    return set()

def append_lines(path: Path, lines):
    with path.open("a") as f:
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
    return f"https://soundcloud.com/{username}/sets/{set_name}"

def extract_likes(username: str):
    return extract_entries(likes_url(username))

def extract_playlist(username: str, set_name: str, is_user_playlist: bool = False):
    return extract_entries(playlist_url(username, set_name, is_user_playlist))

def get_folder_name(username: str, is_likes: bool, set_name: str = None):
    if is_likes:
        return f"{username}-likes"
    return set_name

def download_urls(urls, folder_name: str):
    target_dir = BASE_DIR / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    downloaded_file = target_dir / "downloaded.txt"
    ignored_file = target_dir / "ignored.txt"
    errors_file = target_dir / "errors.txt"

    downloaded = load_set(downloaded_file)
    ignored = load_set(ignored_file)
    seen = downloaded | ignored

    urls = [u for u in urls if u not in seen]

    if not urls:
        logger.info("No new tracks")
        return

    ydl_opts = {
        "outtmpl": str(target_dir / "%(uploader)s - %(title)s"),
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

    append_lines(downloaded_file, success)

    if failed:
        with errors_file.open("a") as f:
            f.write(f"\n\nRun @ {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for url, err in failed:
                f.write(f"{url}\n{err}\n\n")


def run_likes(username: str):
    logger.info(f"Fetching likes for: {username}")
    urls = extract_likes(username)
    folder = get_folder_name(username, is_likes=True)
    download_urls(urls, folder)

def run_playlist(username: str, set_name: str, is_user_playlist: bool = False):
    logger.info(f"Fetching playlist: {username} / {set_name}")
    urls = extract_playlist(username, set_name, is_user_playlist)
    folder = get_folder_name(username, is_likes=False, set_name=set_name)
    download_urls(urls, folder)
