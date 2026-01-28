import os
import time
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import tempfile
import threading

os.environ["PATH"] += os.pathsep + r"C:\Users\sudu6\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.WinGet.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-essentials_build\bin"

model = whisper.load_model("tiny")

_speaking = False
_stop_flag = False
_lock = threading.Lock()


def stop():
    global _stop_flag, _speaking
    with _lock:
        _stop_flag = True
        _speaking = False
    sd.stop()


def speak(text: str):
    global _speaking, _stop_flag
    print(f"COOPER: {text}")
    stop()

    def run():
        global _speaking, _stop_flag
        _stop_flag = False
        _speaking = True

        engine = pyttsx3.init(driverName="sapi5")
        engine.setProperty("rate", 155)
        engine.setProperty("volume", 1.0)
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)

        engine.say(text)

        while engine.isBusy():
            if _stop_flag:
                engine.stop()
                break
            engine.runAndWait()

        engine.stop()
        _speaking = False

    threading.Thread(target=run, daemon=True).start()


def listen(duration: int = 6) -> str:
    fs = 16000
    print("[COOPER] Listening...")
    stop()

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
