from .version import LysnVersion

class LysnHelp():
    def helpFull():
        print(f"""
Lysn - {LysnVersion.version()}

NAVIGATION
  ↑ / ↓        Move selection
  Enter        Open / confirm
  Backspace    Go back
  Ctrl+Q       Exit

PLAYBACK
  Space        Pause / resume
  S            Stop
  R            Restart
  N / B        Next / previous

SEEK
  D / A        +10s / -10s

VOLUME
  W / X        Up / down
  M            Mute

ALBUM
  P            Play album
  Z            Shuffle

Docs: https://github.com/wattox00/lysn
        """)
