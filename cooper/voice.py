import os
import time
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import tempfile

os.environ["PATH"] += os.pathsep + r"C:\Users\sudu6\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-essentials_build\bin"

model = whisper.load_model("tiny")


def _init_tts():
    engine = pyttsx3.init(driverName="sapi5")
    engine.setProperty("rate", 155)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    return engine


def speak(text: str):
    print(f"COOPER: {text}")
    sd.stop()
    time.sleep(0.2)
    engine = _init_tts()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.3)


def listen(duration: int = 6) -> str:
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
            temperature=0.0,
            fp16=False,
            condition_on_previous_text=False
        )
        text = result.get("text", "").strip()
    finally:
        os.remove(audio_path)

    return text
