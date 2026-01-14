import time
import threading

class ProactiveAssistant:
    def __init__(self, callback):
        self.callback = callback
        self.start_time = time.time()
        self.last_suggested = 0

    def start(self):
        def loop():
            while True:
                elapsed = time.time() - self.start_time

                if elapsed > 1800 and time.time() - self.last_suggested > 1800:
                    self.callback(
                        "You have been active for a while. Would you like to take a short break?"
                    )
                    self.last_suggested = time.time()

                time.sleep(30)

        threading.Thread(target=loop, daemon=True).start()
