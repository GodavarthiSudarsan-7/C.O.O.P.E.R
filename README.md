# 🤖 C.O.O.P.E.R – Personal AI Voice Assistant

C.O.O.P.E.R (Conversational Operations & Organized Personal Executive Robot) is a **Python-based personal AI voice assistant** designed to automate system tasks, respond intelligently to user commands, and provide a modular foundation for future AI capabilities.

This project focuses on **clean architecture**, **intent-based command routing**, and **local system control**, making it both a learning project and a strong resume showcase.

---

## 🚀 Features

- 🎙️ Voice command input
- 🧠 Intent detection & routing
- 🔊 System volume control (mute, unmute, etc.)
- ⚡ System power actions (shutdown, restart)
- 💬 AI-based text responses
- 🧩 Modular and extensible design
- 🖥️ Command-line execution
- 🔒 Fully local execution (no cloud dependency by default)

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Language | Python |
| Architecture | Modular (Intent → Router → Action) |
| AI / NLP | Rule-based + AI response module |
| Voice | Speech-to-Text |
| System Control | OS-level commands |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

C.O.O.P.E.R/
│
├── cooper/
│ ├── actions.py # Executes system actions
│ ├── ai_answer.py # AI-based responses
│ ├── intent_router.py # Routes intents to actions
│ ├── intent_rules.py # Intent detection logic
│ ├── personality.py # Assistant personality & responses
│ ├── system_control.py # OS-level system operations
│ ├── shell.py # CLI / shell interface
│ └── voice.py # Voice input handling
│
├── main.py # Entry point
├── .gitignore
├── requirements.txt
└── README.md





---

## 🧠 How C.O.O.P.E.R Works (Logic Flow)

1. 🎤 User gives a voice command
2. 🔍 Speech is converted to text
3. 🧠 Intent is identified using rules
4. 🧭 Intent router selects correct action
5. ⚙️ Action module executes task
6. 💬 AI module responds back to user

---

## ▶️ How to Run the Project Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/GodavarthiSudarsan-7/C.O.O.P.E.R.git
cd C.O.O.P.E.R


 Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

Install dependencies
pip install -r requirements.txt


Run C.O.O.P.E.R
python main.py





📈 Future Enhancements

🧠 Machine Learning–based intent classification

🌍 Online search & browsing

🗂️ Task scheduling

🧑‍💻 GUI / Desktop application

☁️ Cloud-based AI integration

🧠 Memory & personalization