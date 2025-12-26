import sys

from cooper.voice import listen, speak
from cooper.utils import clean_input, normalize_command
from cooper.intent_router import get_intent
from cooper.actions import open_website, open_application
from cooper.ai_answer import answer_question
import sys

from cooper.voice import listen, speak
from cooper.utils import clean_input, normalize_command
from cooper.intent_router import get_intent
from cooper.actions import open_website, open_application
from cooper.ai_answer import answer_question


def get_user_input() -> str:
    """
    Voice first, typing fallback with visible input.
    """
    # 🎙️ Try voice input
    voice_text = listen()

    if voice_text and len(voice_text.split()) >= 2:
        print(f"YOU (voice): {voice_text}")
        return voice_text

    # ⌨️ Voice unclear → typing fallback
    speak("I did not catch that clearly. Please type your command.")

    # 🔑 Force visible typing in terminal
    print("YOU (type): ", end="", flush=True)
    typed = sys.stdin.readline().strip()

    print(f"YOU (type): {typed}")
    return typed


def main():
    # 🔊 Startup
    speak("COOPER is online. Ask me anything or give me a command.")

    while True:
        try:
            user_input = get_user_input()

            if not user_input:
                continue

            # Normalize input
            user_input = normalize_command(clean_input(user_input.lower()))

            # 🛑 Exit commands
            if user_input in ("exit", "quit", "shutdown", "stop cooper"):
                speak("COOPER shutting down. Goodbye.")
                break

            # 🧠 Hybrid intent detection (rules + AI)
            intent = get_intent(user_input)

            # 🚀 ACTION MODE
            if intent["action"] == "open_website":
                open_website(intent["target"])

            elif intent["action"] == "open_application":
                open_application(intent["target"])

            # 🧠 ANSWER MODE (ANY QUESTION)
            else:
                answer = answer_question(user_input)
                print(f"COOPER: {answer}")
                speak(answer)

        except KeyboardInterrupt:
            speak("COOPER shutting down.")
            break

        except Exception as e:
            print("COOPER ERROR:", e)
            speak("An error occurred. Please try again.")


if __name__ == "__main__":
    main()
