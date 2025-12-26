import os
import time
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import tempfile

# ---------- FFmpeg (Windows) ----------
os.environ["PATH"] += os.pathsep + r"C:\Users\sudu6\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-essentials_build\bin"

# ---------- Text-to-Speech ----------
engine = pyttsx3.init(driverName="sapi5")
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# ---------- Whisper ----------
model = whisper.load_model("tiny")


def speak(text: str):
    print(f"COOPER: {text}")
    sd.stop()
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)


def listen(duration: int = 6) -> str:
    """
    High-clarity voice capture tuned for Whisper.
    """
    fs = 16000
    print("[COOPER] Listening...")

    sd.stop()

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    # Normalize volume
    peak = np.max(np.abs(recording))
    if peak > 0:
        recording = recording / peak

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav.write(f.name, fs, recording)
        audio_path = f.name

    try:
        result = model.transcribe(
            audio_path,
            language="en",
            temperature=0.0,        # deterministic
            fp16=False,
            condition_on_previous_text=False,
            no_speech_threshold=0.5
        )
        text = result.get("text", "").strip()
    finally:
        os.remove(audio_path)

    return text
