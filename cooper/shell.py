import sys

from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QPushButton, QScrollArea, QFrame
)

from cooper.assistant.proactive import ProactiveAssistant
from cooper.voice import speak, stop, listen
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
    open_known_folder,
    handle_add_reminder,
    handle_list_reminders,
    handle_set_mode,
    handle_get_mode,
    handle_set_task,
    handle_get_task,
    handle_clear_task
)
from cooper.work.dispatcher import dispatch_work
from cooper.personality import acknowledge, done, confirm_power
from cooper.brain import think
from cooper.ui.theme import STYLESHEET
from cooper.ui.arc_reactor import ArcReactor, STATE_COLORS


class ListenWorker(QThread):
    result_ready = Signal(str)

    def run(self):
        text = listen(duration=6)
        self.result_ready.emit(text)


class CooperShell(QWidget):
    speaking_done = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("CooperShell")
        self.setWindowTitle("C.O.O.P.E.R")
        self.resize(760, 640)
        self.setStyleSheet(STYLESHEET)

        self.chat_mode = False
        self.listen_worker = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        title = QLabel("C . O . O . P . E . R")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        self.reactor = ArcReactor(size=180)
        reactor_row = QHBoxLayout()
        reactor_row.addStretch()
        reactor_row.addWidget(self.reactor)
        reactor_row.addStretch()
        root.addLayout(reactor_row)

        self.status_label = QLabel("ONLINE")
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.status_label)

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setObjectName("ChatScroll")
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setFrameShape(QFrame.NoFrame)

        self.chat_container = QWidget()
        self.chat_container.setObjectName("ChatContainer")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(6, 6, 6, 6)
        self.chat_layout.setSpacing(12)
        self.chat_layout.addStretch(1)

        self.chat_scroll.setWidget(self.chat_container)
        self.chat_scroll.verticalScrollBar().rangeChanged.connect(
            lambda _min, _max: self.chat_scroll.verticalScrollBar().setValue(_max)
        )
        root.addWidget(self.chat_scroll, stretch=1)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.mic_button = QPushButton("\U0001F3A4")
        self.mic_button.setObjectName("MicButton")
        self.mic_button.setFixedSize(44, 44)
        self.mic_button.clicked.connect(self.start_listening)
        input_row.addWidget(self.mic_button)

        self.input = QLineEdit()
        self.input.setObjectName("CommandInput")
        self.input.setPlaceholderText("Your message…")
        self.input.returnPressed.connect(self.handle_input)
        input_row.addWidget(self.input, stretch=1)

        root.addLayout(input_row)

        self.speaking_done.connect(self._on_speaking_done)

        self.say("Initialization complete. COOPER is ready, Boss.")
        self.input.setFocus()

        self.proactive = ProactiveAssistant(self.trigger_proactive)
        self.proactive.start()

    def write(self, text):
        if text.startswith("YOU: "):
            self.add_bubble(text[len("YOU: "):], "user")
        elif text.startswith("COOPER: "):
            self.add_bubble(text[len("COOPER: "):], "cooper")
        else:
            self.add_bubble(text, "cooper")

    def add_bubble(self, text, sender):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setObjectName("BubbleCooper" if sender == "cooper" else "BubbleUser")
        bubble.setMaximumWidth(440)

        avatar = QLabel("C" if sender == "cooper" else "U")
        avatar.setObjectName("AvatarCooper" if sender == "cooper" else "AvatarUser")
        avatar.setFixedSize(30, 30)
        avatar.setAlignment(Qt.AlignCenter)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        if sender == "cooper":
            row.addWidget(avatar)
            row.addWidget(bubble)
            row.addStretch()
        else:
            row.addStretch()
            row.addWidget(bubble)
            row.addWidget(avatar)

        container = QWidget()
        container.setLayout(row)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, container)

    def set_state(self, state: str, label: str = None):
        self.reactor.set_state(state)
        self.status_label.setText(label or state.upper())
        color = STATE_COLORS.get(state, STATE_COLORS["idle"]).name()
        self.status_label.setStyleSheet(f"color: {color};")

    def say(self, message: str):
        self.write(f"COOPER: {message}")
        self.set_state("speaking", "SPEAKING…")
        speak(message, on_done=self.speaking_done.emit)

    def write_reply(self, message: str):
        """Handlers in cooper.actions already speak their own response;
        this just displays it and flashes the speaking state to match."""
        self.write(f"COOPER: {message}")
        self.set_state("speaking", "SPEAKING…")
        duration_ms = max(900, min(6000, int(len(message) * 55)))
        QTimer.singleShot(duration_ms, self._on_speaking_done)

    def _on_speaking_done(self):
        if self.listen_worker is not None and self.listen_worker.isRunning():
            return
        self.set_state("idle", "ONLINE")

    def trigger_proactive(self, text):
        self.say(text)

    def start_listening(self):
        if self.listen_worker is not None and self.listen_worker.isRunning():
            return
        stop()
        self.mic_button.setEnabled(False)
        self.set_state("listening", "LISTENING…")
        self.listen_worker = ListenWorker()
        self.listen_worker.result_ready.connect(self._on_listen_result)
        self.listen_worker.start()

    def _on_listen_result(self, text):
        self.mic_button.setEnabled(True)
        text = text.strip()
        if not text:
            self.set_state("idle", "ONLINE")
            return
        self.write(f"YOU: {text}")
        self.process_command(text)

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

        if text in ("stop", "stop speaking", "quiet", "silence"):
            stop()
            self.set_state("idle", "ONLINE")
            self.write("COOPER: Stopped.")
            return

        if text in ("exit", "quit", "stop cooper"):
            stop()
            self.write("COOPER: Shutting down.")
            speak("Shutting down. Goodbye boss.")
            QApplication.quit()
            return

        intent = get_intent(text)

        if intent["action"] == "chat_mode_on":
            self.chat_mode = True
            self.say("Chat mode activated. I'm listening.")
            return

        elif intent["action"] == "chat_mode_off":
            self.chat_mode = False
            self.say("Back to assistant mode.")
            return

        if self.chat_mode:
            self.set_state("thinking", "THINKING…")
            response = think(text)
            self.say(response)
            return

        if intent["action"] == "set_task":
            response = handle_set_task(intent["target"])
            self.write_reply(response)
            return

        elif intent["action"] == "get_task":
            response = handle_get_task()
            self.write_reply(response)
            return

        elif intent["action"] == "clear_task":
            response = handle_clear_task()
            self.write_reply(response)
            return

        elif intent["action"] == "set_mode":
            response = handle_set_mode(intent["target"])
            self.write_reply(response)
            return

        elif intent["action"] == "get_mode":
            response = handle_get_mode()
            self.write_reply(response)
            return

        elif intent["action"] == "memory_store":
            response = handle_memory_store(intent["target"])
            self.write_reply(response)
            return

        elif intent["action"] == "memory_recall":
            response = handle_memory_recall(intent["target"])
            self.write_reply(response)
            return

        elif intent["action"] == "add_reminder":
            response = handle_add_reminder(intent["target"])
            self.write_reply(response)
            return

        elif intent["action"] == "list_reminders":
            response = handle_list_reminders()
            self.write_reply(response)
            return

        elif intent["action"] == "open_explorer":
            self.say(acknowledge())
            open_file_explorer()
            return

        elif intent["action"] == "open_folder":
            self.say(acknowledge())
            open_known_folder(intent["target"])
            return

        elif intent["action"] == "open_website":
            self.say(acknowledge())
            open_website(intent["target"])
            self.say(done())
            return

        elif intent["action"] == "open_application":
            self.say(acknowledge())
            open_application(intent["target"])
            self.say(done())
            return

        elif intent["action"] == "system_volume":
            self.say(acknowledge())
            system_volume(intent["target"])
            self.say(done())
            return

        elif intent["action"] == "system_power":
            self.say(confirm_power())
            system_power(intent["target"])
            return

        self.set_state("thinking", "THINKING…")
        result = dispatch_work(text)
        if result:
            self.say(result)
            return

        response = think(text)
        self.say(response)


def run_shell():
    app = QApplication(sys.argv)
    window = CooperShell()
    window.show()
    sys.exit(app.exec())
