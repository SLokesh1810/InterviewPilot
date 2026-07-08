import subprocess
import os

from dotenv import load_dotenv

load_dotenv()

FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")

def convert(path: str) -> str:
    """
    Convert any FFmpeg-supported audio/video file
    (mp4, mkv, mp3, m4a, wav, etc.) to mono 16kHz WAV.

    Returns the path to the generated WAV file.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    base, _ = os.path.splitext(path)
    audio_path = base + ".wav"

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", path,
        "-vn",          # Ignore video if present
        "-ac", "1",     # Mono
        "-ar", "16000", # 16 kHz
        audio_path
    ]

    subprocess.run(command, check=True)

    print(f"Audio extracted successfully → {audio_path}")

    return audio_path