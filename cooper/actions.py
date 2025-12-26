import webbrowser
import subprocess
import time
from cooper.voice import speak


def open_website(url: str):
    """
  
    """
    speak("Opening the website.")
    time.sleep(0.3)
    webbrowser.open(url)


def open_application(app_name: str):
    """
 
    """
    apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
    }

    if app_name in apps:
        speak(f"Opening {app_name}.")
        time.sleep(0.3)
        subprocess.Popen([apps[app_name]])
    else:
        speak("I do not know how to open that application yet.")
