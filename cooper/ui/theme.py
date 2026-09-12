BG = "#05070a"
PANEL_BG = "rgba(8, 16, 22, 210)"
BORDER = "#123646"
ACCENT = "#00e5ff"
TEXT = "#c9f7ff"

STYLESHEET = f"""
QWidget#CooperShell {{
    background-color: {BG};
}}

QLabel#StatusLabel {{
    color: {ACCENT};
    font-family: Consolas;
    font-size: 11pt;
    font-weight: bold;
}}

QLabel#TitleLabel {{
    color: {ACCENT};
    font-family: Consolas;
    font-size: 18pt;
    font-weight: bold;
}}

QScrollArea#ChatScroll {{
    background: transparent;
    border: none;
}}

QWidget#ChatContainer {{
    background: transparent;
}}

QLabel#BubbleCooper {{
    background-color: rgba(15, 24, 32, 235);
    border: 1px solid {BORDER};
    border-radius: 14px;
    color: {TEXT};
    font-family: Consolas;
    font-size: 11pt;
    padding: 10px 14px;
}}

QLabel#BubbleUser {{
    background-color: rgba(0, 229, 255, 30);
    border: 1px solid rgba(0, 229, 255, 130);
    border-radius: 14px;
    color: #eafcff;
    font-family: Consolas;
    font-size: 11pt;
    padding: 10px 14px;
}}

QLabel#AvatarCooper {{
    background-color: rgba(0, 229, 255, 35);
    border: 1px solid {ACCENT};
    border-radius: 15px;
    color: {ACCENT};
    font-family: Consolas;
    font-weight: bold;
    font-size: 10pt;
}}

QLabel#AvatarUser {{
    background-color: rgba(255, 255, 255, 18);
    border: 1px solid #3d5a66;
    border-radius: 15px;
    color: {TEXT};
    font-family: Consolas;
    font-weight: bold;
    font-size: 10pt;
}}

QLineEdit#CommandInput {{
    background-color: {PANEL_BG};
    border: 1px solid {ACCENT};
    border-radius: 20px;
    color: #eafcff;
    font-family: Consolas;
    font-size: 12pt;
    padding: 10px 16px;
}}

QPushButton#MicButton {{
    background-color: rgba(0, 229, 255, 25);
    border: 1px solid {ACCENT};
    border-radius: 22px;
    color: {ACCENT};
    font-size: 16pt;
}}

QPushButton#MicButton:hover {{
    background-color: rgba(0, 229, 255, 60);
}}

QPushButton#MicButton:disabled {{
    color: #4a6a75;
    border-color: #2a4650;
    background-color: rgba(0, 229, 255, 8);
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
}}

QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
}}
"""
