import sys
from cooper.voice import listen, speak
from cooper.utils import clean_input, normalize_command
from cooper.intent_router import get_intent
from cooper.actions import open_website, open_application
from cooper.ai_answer import answer_question


def run_shell():
    print("=" * 37)
    print(" COOPER Interactive Shell")
    print("=" * 37)
    print("COOPER online. Type or speak commands.")
    print("Type 'exit' to quit.\n")

    speak("COOPER shell online.")

    while True:
        try:
            print("YOU > ", end="", flush=True)
            typed = sys.stdin.readline().strip()

            if typed:
                user_input = typed
                print(f"YOU > {user_input}")
            else:
                user_input = listen()
                if not user_input:
                    continue
                print(f"YOU > {user_input}")

            user_input = normalize_command(clean_input(user_input.lower()))

            if user_input in ("exit", "quit", "shutdown", "stop cooper"):
                speak("COOPER shutting down.")
                print("COOPER shutting down.")
                break

            if user_input in ("cooper", "hey cooper"):
                speak("Yeah?")
                print("COOPER > Yeah?")
                continue

            intent = get_intent(user_input)

            if intent["action"] == "open_website":
                open_website(intent["target"])
                print("COOPER > Opening website.")

            elif intent["action"] == "open_application":
                open_application(intent["target"])
                print("COOPER > Opening application.")

            else:
                answer = answer_question(user_input)
                speak(answer)
                print(f"COOPER > {answer}")

        except KeyboardInterrupt:
            speak("COOPER shutting down.")
            print("\nCOOPER shutting down.")
            break

        except Exception as e:
            print("COOPER ERROR:", e)
            speak("An error occurred.")
