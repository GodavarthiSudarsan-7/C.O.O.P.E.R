import webbrowser
import subprocess
import time
import os
import urllib.parse
import sqlite3
from datetime import datetime

from cooper.voice import speak
from cooper.memory.memory_manager import MemoryManager

memory = MemoryManager()

DB_PATH = os.path.join(os.path.dirname(__file__), "memory", "memory.db")


class ReminderManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, created_at TEXT)"
        )
        self.conn.commit()

    def add(self, text):
        self.cursor.execute(
            "INSERT INTO reminders VALUES (NULL, ?, ?)",
            (text, datetime.now().isoformat())
        )
        self.conn.commit()

    def list_all(self):
        self.cursor.execute("SELECT text FROM reminders ORDER BY id DESC")
        return [row[0] for row in self.cursor.fetchall()]


reminders = ReminderManager()


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


def open_file_explorer():
    speak("Opening file explorer.")
    subprocess.Popen("explorer", shell=True)


def open_known_folder(folder: str):
    base = os.path.expanduser("~")

    folders = {
        "documents": os.path.join(base, "Documents"),
        "downloads": os.path.join(base, "Downloads"),
        "desktop": os.path.join(base, "Desktop")
    }

    path = folders.get(folder)

    if path and os.path.exists(path):
        speak(f"Opening {folder}.")
        subprocess.Popen(f'explorer "{path}"', shell=True)
    else:
        speak("I cannot find that folder.")


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
            return

        for _ in range(5):
            subprocess.call(
                ["powershell", "-Command", f"(New-Object -ComObject WScript.Shell).SendKeys({key})"],
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


def handle_memory_store(text: str):
    clean = text.lower().replace("remember", "").strip()

    if clean.startswith("my "):
        clean = clean.replace("my ", "", 1)

    if " is " in clean:
        key, value = clean.split(" is ", 1)

    elif len(clean.split()) >= 2:
        parts = clean.split()
        key = parts[0]
        value = " ".join(parts[1:])

    else:
        response = "Tell me clearly what you want me to remember."
        speak(response)
        return response

    key = key.strip()
    value = value.strip()

    memory.remember(
        category="profile",
        key=key,
        value=value
    )

    response = f"Got it. I will remember your {key} is {value}."
    speak(response)
    return response



def handle_memory_recall(text: str):
    if "my name" in text.lower():
        name = memory.recall("name")
        response = f"Your name is {name}." if name else "I don't know your name yet."
        speak(response)
        return response

    response = "I don't have that information yet."
    speak(response)
    return response


def handle_add_reminder(text: str):
    reminder_text = text.lower().replace("remind me", "").strip()
    reminders.add(reminder_text)
    response = f"Got it. I will remind you to {reminder_text}."
    speak(response)
    return response


def handle_list_reminders():
    items = reminders.list_all()
    response = "You have no reminders." if not items else "Your reminders are: " + ", ".join(items) + "."
    speak(response)
    return response
