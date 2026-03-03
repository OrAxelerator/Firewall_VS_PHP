import subprocess
import sys


def play_sound(path, is_audio):
    if is_audio:
        if sys.platform.startswith("win"):# Windows
            import winsound
            winsound.PlaySound(path, winsound.SND_ASYNC)
        elif sys.platform == "darwin":# macOS
            subprocess.Popen(["afplay", path])
        else:# Linux
            subprocess.Popen(
                ["aplay", path],
	            stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
