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
_speak_lock = threading.Lock()


def stop():
    global _stop_flag, _speaking
    with _lock:
        _stop_flag = True
        _speaking = False
    sd.stop()


def speak(text: str, on_done=None):
    global _speaking, _stop_flag
    print(f"COOPER: {text}")
    stop()

    def run():
        global _speaking, _stop_flag
        # SAPI5's COM voice object must be created and used on the same
        # thread, so each call gets its own engine here rather than
        # sharing one across threads. _speak_lock serializes calls so
        # two threads never touch the driver at the same time.
        with _speak_lock:
            _stop_flag = False
            _speaking = True
            try:
                engine = pyttsx3.init(driverName="sapi5")
                engine.setProperty("rate", 155)
                engine.setProperty("volume", 1.0)
                engine.setProperty("voice", engine.getProperty("voices")[0].id)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            finally:
                _speaking = False
                if on_done:
                    on_done()

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
