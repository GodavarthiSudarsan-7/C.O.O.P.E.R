import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from cooper.voice import speak, listen
from cooper.utils import clean_input, normalize_command
from cooper.intent_router import get_intent
from cooper.actions import (
    open_website,
    open_application,
    system_volume,
    system_power,
)
from cooper.ai_answer import answer_question
from cooper.personality import acknowledge, done, confirm_power


class CooperShell:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("COOPER Shell")
        self.root.geometry("700x500")

        self.output = ScrolledText(self.root, state="disabled", wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input = tk.Entry(self.root)
        self.input.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.input.bind("<Return>", self.handle_text_input)

        self.write("COOPER is online. Ready when you are.")
        speak("COOPER is online. Ready when you are.")

        threading.Thread(target=self.voice_loop, daemon=True).start()

    def write(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def handle_text_input(self, event=None):
        text = self.input.get().strip()
        self.input.delete(0, tk.END)
        if text:
            self.write(f"YOU: {text}")
            self.process_command(text)

    def voice_loop(self):
        while True:
            voice = listen()
            if voice:
                self.write(f"YOU (voice): {voice}")
                self.process_command(voice)

    def process_command(self, text):
        text = normalize_command(clean_input(text.lower()))

        if text in ("exit", "quit", "stop cooper"):
            speak("Shutting down. Goodbye.")
            self.root.quit()
            return

        intent = get_intent(text)

        if intent["action"] == "open_website":
            speak(acknowledge())
            open_website(intent["target"])
            speak(done())

        elif intent["action"] == "open_application":
            speak(acknowledge())
            open_application(intent["target"])
            speak(done())

        elif intent["action"] == "system_volume":
            speak(acknowledge())
            system_volume(intent["target"])
            speak(done())

        elif intent["action"] == "system_power":
            speak(confirm_power())
            confirm = listen().lower()
            if "yes" in confirm:
                system_power(intent["target"])
            else:
                speak("Action cancelled.")

        else:
            answer = answer_question(text)
            self.write(f"COOPER: {answer}")
            speak(answer)

    def run(self):
        self.root.mainloop()


def run_shell():
    CooperShell().run()
