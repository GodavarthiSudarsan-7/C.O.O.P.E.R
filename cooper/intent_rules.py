def rule_intent(command: str):
    """
    Fast, offline intent detection
    """
    text = command.lower()

    if "google" in text:
        return {
            "action": "open_website",
            "target": "https://www.google.com"
        }

    if "youtube" in text:
        return {
            "action": "open_website",
            "target": "https://www.youtube.com"
        }

    if "calculator" in text:
        return {
            "action": "open_application",
            "target": "calculator"
        }

    if "notepad" in text:
        return {
            "action": "open_application",
            "target": "notepad"
        }

    return None  # rule failed
