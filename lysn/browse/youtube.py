#!/usr/bin/env python3
import time
import logging
from pathlib import Path
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path.home() / "Music"

def extract_entries(url: str):
    """
    Extracts video URLs from a YouTube playlist or returns the single video.
    """
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if "entries" in info:
        urls = []
        for entry in info["entries"]:
            if not entry:
                continue
            video_url = entry.get("url") or entry.get("webpage_url")
            if video_url:
                if not video_url.startswith("http"):
                    video_url = f"https://www.youtube.com/watch?v={video_url}"
                urls.append(video_url)
        return urls

    return [url]


def get_folder_name(url: str):
    """
    Derive folder name from URL.
    """
    parts = url.rstrip("/").split("/")
    return parts[-1] if len(parts) > 3 else "youtube"


def download_urls(urls, folder_name: str, audio_format: str = "mp3"):
    """
    Download list of URLs as audio.
    """
    target_dir = BASE_DIR / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(target_dir / "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "192",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        for i, url in enumerate(urls, 1):
            logger.info(f"{i}/{len(urls)} downloading")
            try:
                ydl.download([url])
            except Exception:
                pass
            time.sleep(1)

def run_url(url: str, audio_format: str = "mp3"):
    """
    Main entry point: accepts a YouTube URL.
    Handles both playlists and single videos.
    """
    logger.info(f"Processing URL: {url}")

    urls = extract_entries(url)

    if not urls:
        urls = [url]

    folder_name = get_folder_name(url)
    download_urls(urls, folder_name, audio_format)
