import vlc
import random
from pathlib import Path

from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import (
    Static,
    TabbedContent,
    TabPane,
    ListView,
    ListItem,
    Label,
)

# for flags

import argparse
from .flags.update import LysnUpdate
from .flags.version import LysnVersion
from .flags.help import LysnHelp


MUSIC_DIR = Path.home() / "Music"

def song_playing(song):
    return vlc.MediaPlayer(str(song))

class Lysn(App):
    """Lysn"""

    ENABLE_COMMAND_PALETTE = False

    CSS = """
    Screen {
        layout: vertical;
        background: #0b0f14;
        color: #d0d7de;
    }

    #main {
        height: 1fr;
    }

    TabbedContent {
        height: 1fr;
    }

    .tab-box {
        border: round #30363d;
        padding: 1 2;
        background: #0b0f14;
    }

    .list-view {
        height: 1fr;
        background: #0b0f14;
    }

    #player_bar {
        height: 4;
        border-top: solid #30363d;
        padding: 0 1;
        background: #0b0f14;
        color: #c9d1d9;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("enter", "open_item", "Open"),
        Binding("backspace", "go_back", "Back"),
        # Playback
        Binding("space", "pausesong", "Pause / Resume"),
        Binding("s", "stopsong", "Stop"),
        Binding("r", "restartsong", "Restart"),
        Binding("n", "next_song", "Next"),
        Binding("b", "prev_song", "Previous"),
        # Seek
        Binding("d", "forwardsong", "+10s"),
        Binding("a", "backwardsong", "-10s"),
        # Volume
        Binding("w", "volumeup", "Volume Up"),
        Binding("x", "volumedown", "Volume Down"),
        Binding("m", "volumemute", "Mute"),
        # Album
        Binding("p", "play_album", "Play Album"),
        Binding("z", "shuffle_album", "Shuffle Album"),
        # UI
        Binding("down", "focus_tab_content", "Enter Tab"),
    ]

    def format_key(self, key: str) -> str:
        """Make keys human-friendly."""
        key = key.replace("ctrl+", "Ctrl+")
        return key.capitalize() if len(key) > 1 else key.upper()

    def generate_help(self) -> str:
        """Generate dynamic help text."""

        sections = {
            "Navigation": ["quit", "open_item", "go_back", "focus_tab_content"],
            "Playback": ["pausesong", "stopsong", "restartsong", "next_song", "prev_song"],
            "Seek": ["forwardsong", "backwardsong"],
            "Volume": ["volumeup", "volumedown", "volumemute"],
            "Album": ["play_album", "shuffle_album"],
        }

        lines = [f"[bold]Lysn[/] - {LysnVersion.version()}", ""]

        for section, actions in sections.items():
            lines.append(f"[bold]{section.upper()}[/]")

            for action in actions:
                for binding in self.BINDINGS:
                    if binding.action == action:
                        key = self.format_key(binding.key)
                        lines.append(f"  [cyan]{key:<10}[/] {binding.description}")

            lines.append("")

        lines.append("[dim]Docs: https://github.com/wattox00/lysn[/]")

        return "\n".join(lines)

    def compose(self) -> ComposeResult:
        with Container(id="main"):
            with TabbedContent(id="tabs"):

                with TabPane("Albums", id="albums_tab"):
                    self.album_list = ListView(classes="tab-box")
                    yield self.album_list

                with TabPane("Browse", id="browse_tab"):
                    self.browser_list = ListView(classes="tab-box")
                    yield self.browser_list

                with TabPane("Help"):
                    with VerticalScroll():
                        yield Static(
                            self.generate_help(),
                            classes="tab-box",
                            markup=True,
                        )

        self.player_text = Static("No song playing", id="player_bar")
        yield self.player_text

    def on_mount(self) -> None:
        self.current_path = MUSIC_DIR
        self.history = []
        self.browser_mode = "root"
        self.refresh_list()
        self.refresh_browser()
        self.set_interval(0.5, self.player_tick)
        self.muted = False
        self.sc_user = "your_username"
        self.sc_set = "your_playlist"
        self.input_mode = None
        self.input_buffer = ""
        self.pending_action = None

    def action_quit(self):
        self.exit()

    def get_active_tab(self):
        tabs = self.query_one("#tabs", TabbedContent)
        return tabs.active

    def player_tick(self):
        if not hasattr(self, "player"):
            return

        if hasattr(self, "playlist"):
            state = self.player.get_state()
            if state == vlc.State.Ended:
                self.action_next_song()
                return

        state = self.player.get_state()

        icon = {
            vlc.State.Playing: "▶",
            vlc.State.Paused: "▮▮",
        }.get(state, "•")

        current = self.player.get_time()
        total = self.player.get_length()

        if current <= 0 or total <= 0:
            return

        current //= 1000
        total //= 1000

        progress = current / total
        bar_len = 30
        filled = int(progress * bar_len)

        bar = "━" * filled + "·" * (bar_len - filled)

        def fmt(t):
            return f"{t//60:02}:{t%60:02}"

        time_str = f"{fmt(current)} / {fmt(total)}"

        vol = getattr(self, "volume", 0)
        muted = getattr(self, "muted", False)
        vol_str = "M" if muted else f"{vol}%"

        song = getattr(self, "_current_song_name", "No song")

        line1 = f"{icon}  {song[:40]}"
        line2 = f"{fmt(current)} {bar} {fmt(total)}  {vol_str}"

        new_text = f"{line1}\n{line2}"

        if getattr(self, "_last_player_bar", None) != new_text:
            self._last_player_bar = new_text
            self.player_text.update(new_text)

    # Player
    def play_song_list(self, songs):
        if not songs:
            return

        if getattr(self, "playlist", None) == songs:
            return

        self.playlist = songs
        self.current_index = 0
        self.play_current_song()

    def play_current_song(self):
        if not hasattr(self, "playlist") or not self.playlist:
            return

        song = self.playlist[self.current_index]

        if not hasattr(self, "player"):
            self.player = vlc.MediaPlayer()

        else:
            self.player.stop()

        media = vlc.Media(str(song))
        self.player.set_media(media)

        self.volume = getattr(self, "volume", 50)
        self.player.audio_set_volume(self.volume)
        self.player.play()

        self._current_song_name = song.stem
        self.player_text.update(f"Playing: {self._current_song_name}")

    # Album Nav
    def refresh_list(self):
        items = sorted(
            self.current_path.iterdir(),
            key=lambda x: (x.is_file(), x.name.lower())
        )

        if getattr(self, "_last_album_items", None) == items:
            return

        self._last_album_items = items
        self.album_list.clear()

        for item in items:
            label = f"[DIR] {item.name}" if item.is_dir() else item.name
            self.album_list.append(ListItem(Label(label)))

    def open_album_item(self):
        if self.album_list.index is None:
            return

        items = sorted(self.current_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        selected = items[self.album_list.index]

        if selected.is_dir():
            self.history.append(self.current_path)
            self.current_path = selected
            self.refresh_list()

    def action_go_back(self) -> None:
        if self.get_active_tab() == "albums_tab":
            if self.history:
                self.current_path = self.history.pop()
                self.refresh_list()

        elif self.get_active_tab() == "browse_tab":
            if self.browser_mode == "soundcloud_menu":
                self.browser_mode = "root"
                self.refresh_browser()

    def get_album_songs(self):
        return [f for f in self.current_path.iterdir() if f.is_file()]

    def action_play_album(self) -> None:
        if self.current_path == MUSIC_DIR:
            return

        songs = sorted(self.get_album_songs())
        self.play_song_list(songs)

    def action_shuffle_album(self) -> None:
        if self.current_path == MUSIC_DIR:
            return

        songs = self.get_album_songs()
        random.shuffle(songs)
        self.play_song_list(songs)

    def action_focus_tab_content(self):
        if self.get_active_tab() == "albums_tab":
            self.album_list.focus()
        elif self.get_active_tab() == "browse_tab":
            self.browser_list.focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view is self.album_list:
            self.open_album_item()
        elif event.list_view is self.browser_list:
            self.open_browser_item()

    # Browse
    def refresh_browser(self):
        self.browser_list.clear()

        if self.browser_mode == "root":
            options = ["SoundCloud", "Spotify"]
        elif self.browser_mode == "soundcloud_menu":
            options = ["Likes", "Albums", "Song"]
        else:
            options = []

        for opt in options:
            item = ListItem(Label(opt))
            item.data = opt
            self.browser_list.append(item)

    def open_browser_item(self):
        if self.browser_list.index is None:
            return

        item = self.browser_list.children[self.browser_list.index]
        label = item.data

        if self.browser_mode == "root":
            if label == "SoundCloud":
                self.browser_mode = "soundcloud_menu"
                self.refresh_browser()

        elif self.browser_mode == "soundcloud_menu":
            if label == "Likes":
                self.input_mode = "username"
                self.pending_action = "likes"

            elif label == "Albums":
                self.input_mode = "username"
                self.pending_action = "album"

            elif label == "Song":
                self.input_mode = "username"
                self.pending_action = "song"

    def action_open_item(self) -> None:
        if self.get_active_tab() == "albums_tab":
            self.open_album_item()
        elif self.get_active_tab() == "browse_tab":
            self.open_browser_item()

    # prompt typing
    def on_key(self, event):
        if not self.input_mode:
            return

        from lysn.browse.soundcloud import run_likes, run_playlist, run_songs

        if event.key == "enter":

            if self.input_mode == "username":
                if not self.input_buffer.strip():
                    self.player_text.update("Please enter a username:")
                    return

                self.temp_username = self.input_buffer.strip()
                self.input_buffer = ""

                if self.pending_action == "likes":
                    self.player_text.update("Downloading likes...")
                    run_likes(self.temp_username)
                    self.player_text.update(f"Done: {self.temp_username}")

                    self.input_mode = None
                    self.pending_action = None

                else:
                    self.input_mode = "setname"
                    self.player_text.update("Enter name:")

            elif self.input_mode == "setname":
                if not self.input_buffer.strip():
                    self.player_text.update("Please enter a name:")
                    return

                setname = self.input_buffer.strip()
                self.input_buffer = ""

                self.player_text.update("Downloading...")

                if self.pending_action == "album":
                    run_playlist(self.temp_username, setname)

                elif self.pending_action == "song":
                    run_songs(self.temp_username, setname)

                self.player_text.update(f"Done: {setname}")

                self.input_mode = None
                self.pending_action = None
                self.temp_username = None

        elif event.key == "backspace":
            self.input_buffer = self.input_buffer[:-1]

        elif event.character:
            self.input_buffer += event.character

        self.player_text.update(f"> {self.input_buffer}")

    # Player bar
    def action_playsong(self) -> None:
        self.play_current_song()

    def action_stopsong(self) -> None:
        if hasattr(self, "player"):
            self.player.stop()

    def action_pausesong(self) -> None:
        if hasattr(self, "player"):
            self.player.pause()

    def action_restartsong(self) -> None:
        if hasattr(self, "player"):
            self.player.set_time(0)

    def action_forwardsong(self) -> None:
        if hasattr(self, "player"):
            self.player.set_time(self.player.get_time() + 10000)

    def action_backwardsong(self) -> None:
        if hasattr(self, "player"):
            self.player.set_time(self.player.get_time() - 10000)

    def action_volumeup(self) -> None:
        if hasattr(self, "player"):
            self.volume = min(self.volume + 5, 100)
            self.player.audio_set_volume(self.volume)

    def action_volumedown(self) -> None:
        if hasattr(self, "player"):
            self.volume = max(self.volume - 5, 0)
            self.player.audio_set_volume(self.volume)

    def action_volumemute(self) -> None:
        if hasattr(self, "player"):
            self.muted = not self.muted
            self.player.audio_set_mute(self.muted)

    def action_next_song(self) -> None:
        if not hasattr(self, "playlist") or not self.playlist:
            return

        self.current_index += 1
        if self.current_index >= len(self.playlist):
            self.current_index = 0

        self.play_current_song()

    def action_prev_song(self) -> None:
        if not hasattr(self, "playlist") or not self.playlist:
            return

        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1

        self.play_current_song()

def parse_args():
    parser = argparse.ArgumentParser(
        prog="lysn",
        description=f"{LysnVersion.version()}\nTUI Music Player :)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-hf", "--helpf", action="store_true", help="show full help message and exit")

    info = parser.add_argument_group("Information")
    info.add_argument("-u", "--update", action="store_true", help="update lysn with pipx")
    info.add_argument("-v", "--version", action="store_true", help="show version and exit")

    return parser.parse_args()

def main():
    args = parse_args()
 
    if args.helpf:
        LysnHelp.helpFull()
        return

    if args.update:
        LysnUpdate.update()
        return

    if args.version:
        print(LysnVersion.version())
        return
    app = Lysn()
    app.run()

if __name__ == "__main__":
    main()
