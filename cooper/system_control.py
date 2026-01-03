import os
import subprocess
import webbrowser
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def open_application(app: str) -> str:
    apps = {
        "chrome": "chrome",
        "google chrome": "chrome",
        "notepad": "notepad",
        "calculator": "calc",
        "cmd": "cmd",
        "powershell": "powershell",
        "vs code": "code",
        "visual studio code": "code"
    }

    for key, command in apps.items():
        if key in app:
            subprocess.Popen(command, shell=True)
            return f"Opening {key}"

    return "I could not find that application."


def open_website(site: str) -> str:
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com",
        "gmail": "https://mail.google.com"
    }

    for key, url in sites.items():
        if key in site:
            webbrowser.open(url)
            return f"Opening {key}"

    if site.startswith("http"):
        webbrowser.open(site)
        return "Opening website"

    return "I could not recognize the website."


def volume_control(action: str) -> str:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current = volume.GetMasterVolumeLevelScalar()

    if "up" in action:
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
        return "Volume increased"

    if "down" in action:
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
        return "Volume decreased"

    if "mute" in action:
        volume.SetMute(1, None)
        return "Volume muted"

    if "unmute" in action:
        volume.SetMute(0, None)
        return "Volume unmuted"

    return "Volume command not recognized"


def power_control(action: str) -> str:
    if "shutdown" in action:
        os.system("shutdown /s /t 5")
        return "System will shut down in five seconds"

    if "restart" in action:
        os.system("shutdown /r /t 5")
        return "System will restart in five seconds"

    return "Power command not recognized"
