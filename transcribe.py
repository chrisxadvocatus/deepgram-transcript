from pathlib import Path
import os
import requests


DEEPGRAM_API_KEY = "--"

BASE_DIR = Path(__file__).parent

AUDIO_FILE = BASE_DIR / "audio" / "--.mp3"
OUTPUT_DIR = BASE_DIR / "transcripts"


def transcribe_audio(audio_path: Path) -> dict:
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    response = requests.post(
        "https://api.deepgram.com/v1/listen",
        params={
            "model": "nova-3",
            "language": "zh",
            "smart_format": "true"
        },
        headers={
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/mpeg",
        },
        data=audio_path.read_bytes(),
        timeout=120,
    )

    response.raise_for_status()
    return response.json()


def save_transcript(result: dict, audio_path: Path):
    transcript = (
        result["results"]["channels"][0]["alternatives"][0]["transcript"]
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # recording.mp3 -> recording.txt
    output_file = OUTPUT_DIR / f"{audio_path.stem}.txt"

    output_file.write_text(transcript, encoding="utf-8")

    print(f"Transcript saved to: {output_file}")


if __name__ == "__main__":
    result = transcribe_audio(AUDIO_FILE)

    save_transcript(result, AUDIO_FILE)
