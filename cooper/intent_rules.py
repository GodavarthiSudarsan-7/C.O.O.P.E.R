def rule_intent(command: str):
    text = command.lower()

    if "open google" in text:
        return {"action": "open_website", "target": "https://www.google.com"}

    if "open youtube" in text:
        return {"action": "open_website", "target": "https://www.youtube.com"}

    if "open calculator" in text:
        return {"action": "open_application", "target": "calculator"}

    if "open notepad" in text:
        return {"action": "open_application", "target": "notepad"}

    if "increase volume" in text or "volume up" in text:
        return {"action": "system_volume", "target": "up"}

    if "decrease volume" in text or "volume down" in text:
        return {"action": "system_volume", "target": "down"}

    if "mute volume" in text or "mute system" in text:
        return {"action": "system_volume", "target": "mute"}

    if "shutdown system" in text or "shut down computer" in text:
        return {"action": "system_power", "target": "shutdown"}

    if "restart system" in text or "restart computer" in text:
        return {"action": "system_power", "target": "restart"}

    return None
