# Lysn - CLI Music Player

[![Version](https://img.shields.io/badge/version-0.2.5-blue?style=for-the-badge)](https://github.com/WattoX00/lysn/releases/tag/v0.2.5)
![Python](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge)
[![PyPI](https://img.shields.io/pypi/v/lysn?style=for-the-badge)](https://pypi.org/project/lysn/)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
![Build](https://img.shields.io/github/actions/workflow/status/wattox00/lysn/publish.yml?style=for-the-badge)
[![License](https://img.shields.io/github/license/wattox00/lysn?style=for-the-badge)](https://github.com/WattoX00/lysn/blob/main/LICENSE)

<details>
<summary>📚 Contents</summary>
 
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Music Directory](#music-directory)
- [Interface Overview](#interface-overview)
- [Support](#support)
- [License](#license)

</details>

## Installation

```bash
pip install lysn
```

> [!IMPORTANT]
> `todol` is a terminal application. I recommend installing it with `pipx`.

# Usage

Run the application:

```bash
lysn
```

## Controls
<details>
<summary>See all</summary>
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

</details>

## Music Directory
Place all your music inside the `~/Music` directory on your system.
Albums are detected as subfolders inside `~/Music`.
Supported formats depend on your system’s audio backend.

## Interface Overview

### 📀 Album Tab
- Reads your `~/Music` directory.
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
- Downloads go into `~/Music`.
- The app may appear frozen during download - this is normal.
- In some cases, progress may not appear in the UI.

### ❓ Help Tab
- Displays all keybindings inside the app.

## Flags
```bash
lysn --help
lysn --helpf
lysn --version
lysn --update
```

## 📝 Notes
- All downloaded content is saved to `~/Music`.
- Make sure names match exactly with SoundCloud URLs.

Enjoy your music - right from the terminal.

## Support

If this project saved you time, taught you something, or made your day a little easier,
you can support its development here:

👉 **[Buy me a coffee via PayPal](https://www.paypal.com/paypalme/wattox)**

Your support helps keep the project:
- Actively maintained
- Continuously improved
- Free and open source

Thanks for being part of the community 🤝

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.
