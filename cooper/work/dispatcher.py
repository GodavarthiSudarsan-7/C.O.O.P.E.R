import os
import subprocess
import webbrowser

HOME = os.path.expanduser("~")

PROJECTS = {
    "mini project": os.path.join(HOME, "Projects", "mini-project"),
    "daa": os.path.join(HOME, "Documents", "DAA")
}

def dispatch_work(command: str):
    command = command.lower()

    if "start work" in command:
        subprocess.Popen("code", shell=True)
        return "Starting work environment."

    if "open my project" in command or "open mini project" in command:
        path = PROJECTS.get("mini project")
        if path and os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"', shell=True)
            subprocess.Popen("code", shell=True)
            return "Opening your project."

    if "code now" in command:
        subprocess.Popen("code", shell=True)
        return "Opening code editor."

    if "run code" in command or "compile code" in command:
        subprocess.Popen("cmd.exe", shell=True)
        return "Opening terminal."

    if "study daa" in command:
        webbrowser.open("https://nptel.ac.in")
        return "Opening study resources."

    return None
