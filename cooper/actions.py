import webbrowser
import subprocess
import time
from cooper.voice import speak
import os


def open_website(url: str):
    speak("Opening website.")
    webbrowser.open(url)


def open_application(app_name: str):
    apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe"
    }

    if app_name in apps:
        speak(f"Opening {app_name}.")
        subprocess.Popen([apps[app_name]])
    else:
        speak("I cannot open that application.")


def system_volume(action: str):
    if action == "up":
        speak("Increasing volume.")
        for _ in range(5):
            subprocess.call(
                ["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.05)

    elif action == "down":
        speak("Decreasing volume.")
        for _ in range(5):
            subprocess.call(
                ["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.05)

    elif action == "mute":
        speak("Muting volume.")
        subprocess.call(
            ["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def system_power(action: str):
    if action == "shutdown":
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")

    elif action == "restart":
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")
