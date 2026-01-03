import webbrowser
import subprocess
import time
import os
from cooper.voice import speak


def open_website(url: str):
    speak("Opening website.")
    try:
        webbrowser.open(url)
    except Exception:
        speak("I was unable to open the website.")


def open_application(app_name: str):
    apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe"
    }

    if app_name in apps:
        speak(f"Opening {app_name}.")
        try:
            subprocess.Popen(apps[app_name], shell=True)
        except Exception:
            speak("I could not open the application.")
    else:
        speak("I cannot open that application.")


def system_volume(action: str):
    try:
        if action == "up":
            speak("Increasing volume.")
            key = "[char]175"

        elif action == "down":
            speak("Decreasing volume.")
            key = "[char]174"

        elif action == "mute":
            speak("Muting volume.")
            key = "[char]173"

        else:
            speak("Volume command not recognized.")
            return

        for _ in range(5):
            subprocess.call(
                [
                    "powershell",
                    "-Command",
                    f"(New-Object -ComObject WScript.Shell).SendKeys({key})"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.05)

    except Exception:
        speak("I could not control the volume.")


def system_power(action: str):
    if action == "shutdown":
        speak("Shutting down the system in five seconds.")
        os.system("shutdown /s /t 5")

    elif action == "restart":
        speak("Restarting the system in five seconds.")
        os.system("shutdown /r /t 5")

    else:
        speak("Power command not recognized.")
