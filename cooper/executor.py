from cooper.actions import (
    open_website,
    open_application,
    google_search,
    youtube_play,
    write_text,
)
from cooper.voice import speak


def execute_steps(steps):
    for step in steps:
        action = step.get("action")
        target = step.get("target")

        speak("On it.")

        if action == "open_website":
            open_website(target)

        elif action == "open_application":
            open_application(target)

        elif action == "google_search":
            google_search(target)

        elif action == "youtube_play":
            youtube_play()

        elif action == "write_text":
            write_text(target)

        else:
            speak("I cannot perform that step.")
