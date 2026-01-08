from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit
)
import sys

from cooper.voice import speak
from cooper.utils import clean_input, normalize_command
from cooper.intent_router import get_intent
from cooper.actions import (
    open_website,
    open_application,
    system_volume,
    system_power,
    handle_memory_store,
    handle_memory_recall,
    open_file_explorer,
    open_known_folder
)
from cooper.ai_answer import answer_question
from cooper.personality import acknowledge, done, confirm_power


class CooperShell(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("COOPER Shell")
        self.resize(800, 500)

        layout = QVBoxLayout(self)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command and press Enter…")
        self.input.returnPressed.connect(self.handle_input)
        layout.addWidget(self.input)

        self.write("Initialization complete. COOPER is ready, Boss.")
        speak("Initialization complete. COOPER is ready, Boss.")

        self.input.setFocus()

    def write(self, text):
        self.output.append(text)

    def handle_input(self):
        text = self.input.text().strip()
        self.input.clear()

        if not text:
            return

        self.write(f"YOU: {text}")
        self.process_command(text)
        self.input.setFocus()

    def process_command(self, text):
        text = normalize_command(clean_input(text.lower()))

        if text in ("exit", "quit", "stop cooper"):
            self.write("COOPER: Shutting down.")
            speak("Shutting down. Goodbye boss.")
            QApplication.quit()
            return

        intent = get_intent(text)

        if intent["action"] == "memory_store":
            response = handle_memory_store(intent["target"])
            self.write(f"COOPER: {response}")
            return

        elif intent["action"] == "memory_recall":
            response = handle_memory_recall(intent["target"])
            self.write(f"COOPER: {response}")
            return

        elif intent["action"] == "open_explorer":
            msg = acknowledge()
            self.write(f"COOPER: {msg}")
            speak(msg)
            open_file_explorer()
            return

        elif intent["action"] == "open_folder":
            msg = acknowledge()
            self.write(f"COOPER: {msg}")
            speak(msg)
            open_known_folder(intent["target"])
            return

        elif intent["action"] == "open_website":
            msg = acknowledge()
            self.write(f"COOPER: {msg}")
            speak(msg)
            open_website(intent["target"])
            msg = done()
            self.write(f"COOPER: {msg}")
            speak(msg)

        elif intent["action"] == "open_application":
            msg = acknowledge()
            self.write(f"COOPER: {msg}")
            speak(msg)
            open_application(intent["target"])
            msg = done()
            self.write(f"COOPER: {msg}")
            speak(msg)

        elif intent["action"] == "system_volume":
            msg = acknowledge()
            self.write(f"COOPER: {msg}")
            speak(msg)
            system_volume(intent["target"])
            msg = done()
            self.write(f"COOPER: {msg}")
            speak(msg)

        elif intent["action"] == "system_power":
            msg = confirm_power()
            self.write(f"COOPER: {msg}")
            speak(msg)
            system_power(intent["target"])

        else:
            try:
                from cooper.planner import plan_steps
                from cooper.executor import execute_steps

                self.write("COOPER: Planning steps.")
                speak("Let me think.")

                steps = plan_steps(text)
                execute_steps(steps)

                self.write("COOPER: Done.")
                speak("Done.")

            except Exception:
                answer = answer_question(text)
                self.write(f"COOPER: {answer}")
                speak(answer)


def run_shell():
    app = QApplication(sys.argv)
    window = CooperShell()
    window.show()
    sys.exit(app.exec())
