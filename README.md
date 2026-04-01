# Lysn — CLI Music Player

**Lysn** is a lightweight, terminal-based music player with built-in downloading support.  
It’s designed for speed, simplicity, and full keyboard control.

## ✨ Features

- ▶️ Play local audio files from `/Music`
- ⬇️ Download music from SoundCloud (users, playlists, albums, songs)
- ⌨️ Fast, keyboard-driven interface
- 📀 Album-based playback
- 🔀 Shuffle support
- 🚧 Upcoming: Spotify integration

## 📦 Installation

```bash
pip install lysn
```

# 🚀 Usage

Run the application:

```bash
lysn
```
## 🎮 Controls
### Navigation

| Key       | Action         |
| --------- | -------------- |
| ↑ / ↓     | Move selection |
| Enter     | Open / Confirm |
| Backspace | Go back        |

### Playback

| Key   | Action         |
| ----- | -------------- |
| Space | Pause / Resume |
| S     | Stop           |
| R     | Restart song   |
| N     | Next song      |
| B     | Previous song  |

### Seeking

| Key | Action              |
| --- | ------------------- |
| D   | Forward 10 seconds  |
| A   | Backward 10 seconds |

### Volume

| Key | Action      |
| --- | ----------- |
| W   | Volume up   |
| X   | Volume down |
| M   | Mute toggle |

### Album Actions

| Key | Action        |
| --- | ------------- |
| P   | Play album    |
| Z   | Shuffle album |

### Quit
|  Key   | Action           |
|  ---   | ---------------- |
| Ctrl+Q | Exit application |


## 📁 Music Directory
Place all your music inside the /Music directory.
Albums are detected as subfolders inside /Music.
Supported formats depend on your system’s audio backend.

## 🧭 Interface Overview

### 📀 Album Tab
- Reads your /Music directory.
- Subfolders are treated as albums.
- Enter an album to view tracks.
- Press:
   - P → Play album
   - Z → Shuffle album
- Press Backspace to return.

### 🌐 Browse Tab (Downloads)

Currently supports SoundCloud only.

Available options:

- Likes
- Playlists / Albums
- Single Song

Enter only the exact names from the URL. You can paste in with CTRL+V

### Examples:

#### Likes:
url: `https://soundcloud.com/mjimmortal/likes`
```
username: mjimmortal
```

#### Playlist / Album:
url: `https://soundcloud.com/mjimmortal/sets/thriller-40`

```
username: mjimmortal
playlist/album: thriller-40
```

#### Song download:
url: `https://soundcloud.com/mjimmortal/billie-jean-single-version`

```
username: mjimmortal
song: billie-jean-single-version
```

#### Download Behavior
- Downloads go into /Music.
- The app may appear frozen during download - this is normal.
- In some cases, progress may not appear in the UI.

### ❓ Help Tab
- Displays all keybindings inside the app.

## ⚙️ CLI Flags
```bash
lysn --help
lysn --helpf
lysn --version
lysn --update
```

## 📝 Notes
- All downloaded content is saved to /Music.
- Make sure names match exactly with SoundCloud URLs.
- Performance depends on your system and audio backend.

Enjoy your music - right from the terminal.
