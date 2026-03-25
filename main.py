import vlc
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TabbedContent, TabPane
from textual.containers import Container
from textual.binding import Binding

folder = '/home/wattox/Documents/lysn/songs/'
song = folder + '3.m4a'

def song_playing(song):
    return vlc.MediaPlayer(song)


class Lysn(App):
    """Lysn"""

    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 1fr;
    }

    TabbedContent {
        height: 1fr;
    }

    .tab-box {
        border: round green;
        padding: 1 2;
    }

    #player_bar {
        height: 3;
        border-top: solid green;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("e", "playsong", "Play Song"),
        Binding("s", "stopsong", "Stop Song"),
        Binding("space", "pausesong", "Pause Song"),
        Binding("r", "restartsong", "Restart Song"),
        Binding("right", "forwardsong", "Seek 10 sec"),
        Binding("left", "backwardsong", "Go back 10 sec"),
        Binding("up", "volumeup", "Volume Up"),
        Binding("down", "volumedown", "Volume Down"),
        Binding("m", "volumemute", "Mute"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="main"):
            with TabbedContent():
                with TabPane("Download"):
                    yield Static("Download tab content", classes="tab-box", id="download_tab")

                with TabPane("Albums"):
                    yield Static("Albums tab content", classes="tab-box", id="albums_tab")

                with TabPane("Guide"):
                    yield Static("Guide tab content", classes="tab-box", id="guide_tab")

        self.player_text = Static("No song playing", id="player_bar")
        yield self.player_text

        yield Footer()

    def action_playsong(self) -> None:
        self.player = song_playing(song)
        self.volume = 90
        self.player.audio_set_volume(self.volume)
        self.player.play()
        self.player_text.update(f"Playing: {song}")

    def action_stopsong(self) -> None:
        if hasattr(self, "player"):
            self.player.stop()
        self.player_text.update(f"Stopped: {song}")

    def action_pausesong(self) -> None:
        if hasattr(self, "player"):
            self.player.pause()
        self.player_text.update(f"Paused: {song}")

    def action_restartsong(self) -> None:
        if hasattr(self, "player"):
            self.player.set_time(0)
        self.player_text.update(f"Restarted: {song}")

    def action_forwardsong(self) -> None:
        if hasattr(self, "player"):
            self.player.set_time(self.player.get_time() + 10000)
        self.player_text.update("Forward 10s")

    def action_backwardsong(self) -> None:
        if hasattr(self, "player"):
            self.player.set_time(self.player.get_time() - 10000)
        self.player_text.update("Back 10s")

    def action_volumeup(self) -> None:
        if hasattr(self, "player"):
            self.volume += 5
            self.player.audio_set_volume(self.volume)
        self.player_text.update(f"Volume: {self.volume}")

    def action_volumedown(self) -> None:
        if hasattr(self, "player"):
            self.volume -= 5
            self.player.audio_set_volume(self.volume)
        self.player_text.update(f"Volume: {self.volume}")

    def action_volumemute(self) -> None:
        if hasattr(self, "player"):
            self.player.audio_toggle_mute()
        self.player_text.update("Muted toggle")


if __name__ == "__main__":
    app = Lysn()
    app.run()
