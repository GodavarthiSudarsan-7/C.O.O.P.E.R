def rule_intent(text: str):
    text = text.lower()

    if text.startswith("remember"):
        return {"action": "memory_store", "target": text}

    if "my name" in text or "what do you know about me" in text:
        return {"action": "memory_recall", "target": text}

    if "open file explorer" in text or "open explorer" in text:
        return {"action": "open_explorer", "target": None}

    if "open documents" in text:
        return {"action": "open_folder", "target": "documents"}

    if "open downloads" in text:
        return {"action": "open_folder", "target": "downloads"}

    if "open google" in text:
        return {"action": "open_website", "target": "https://www.google.com"}

    if "open youtube" in text:
        return {"action": "open_website", "target": "https://www.youtube.com"}

    if "open github" in text:
        return {"action": "open_website", "target": "https://www.github.com"}

    if "open calculator" in text or "open calc" in text:
        return {"action": "open_application", "target": "calculator"}

    if "open notepad" in text:
        return {"action": "open_application", "target": "notepad"}

    if "open chrome" in text:
        return {"action": "open_application", "target": "chrome"}

    if "volume up" in text or "increase volume" in text:
        return {"action": "system_volume", "target": "up"}

    if "volume down" in text or "decrease volume" in text:
        return {"action": "system_volume", "target": "down"}

    if "mute volume" in text or "mute system" in text:
        return {"action": "system_volume", "target": "mute"}

    if "shutdown system" in text or "shut down computer" in text:
        return {"action": "system_power", "target": "shutdown"}

    if "restart system" in text or "restart computer" in text:
        return {"action": "system_power", "target": "restart"}

    return None
