from .version import LysnVersion

class LysnHelp():
    def helpFull():
        print(f"""
{LysnVersion.version()}
NAVIGATION
----------
[↑ / ↓]        Move selection
[Enter]        Open item / Confirm
[Backspace]    Go back

PLAYBACK CONTROLS
-----------------
[Space]        Pause / Resume
[S]            Stop
[R]            Restart song
[N]            Next song
[B]            Previous song

SEEKING
-------
[D]            Forward 10 seconds
[A]            Backward 10 seconds

VOLUME
------
[W]            Volume up
[X]            Volume down
[M]            Mute toggle

ALBUM ACTIONS
-------------
[P]            Play album
[Z]            Shuffle album

QUIT
----
[Q]            Exit application

FOR MORE CHECK OUT THE FULL DOCUMENTATION ON:
https://github.com/wattox00/lysn
        """)
