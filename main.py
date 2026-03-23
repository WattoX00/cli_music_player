import vlc
import time
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container
from textual.binding import Binding

song = '/home/wattox/Documents/cli_music_player/songs/3.m4a'

def song_playing(song):
    return vlc.MediaPlayer(song)

class MyApp(App):
    """Lysn"""

    CSS = """
    Screen {
        align: center middle;
    }

    #box {
        border: round green;
        padding: 1 2;
        width: 50%;
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
    ]

    def compose(self) -> ComposeResult:
        """Create UI layout."""
        yield Header()
        with Container(id="box"):
            self.text = Static("Lysn")
            yield self.text
        yield Footer()

    def action_playsong(self) -> None:
        self.text.update(f"song playing: {song}.")
        self.player = song_playing(song)
        self.player.play()

    def action_stopsong(self) -> None:
        self.text.update(f"song STOPED: {song}.")
        self.player.stop()

    def action_pausesong(self) -> None:
        self.text.update(f"song PAUSED: {song}.")
        self.player.pause()

    def action_restartsong(self) -> None:
        self.text.update(f"song Restarted: {song}.")
        self.player.set_time(0)

    def action_forwardsong(self) -> None:
        self.text.update(f"song Forwarded: {song}.")
        self.player.set_time(self.player.get_time() + 10000)

    def action_backwardsong(self) -> None:
        self.text.update(f"song Backwarded: {song}.")
        self.player.set_time(self.player.get_time() - 10000)

if __name__ == "__main__":
    app = MyApp()
    app.run()

