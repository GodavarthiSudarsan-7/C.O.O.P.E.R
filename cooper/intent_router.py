from cooper.intent_rules import rule_intent

def get_intent(command: str):
    intent = rule_intent(command)
    if intent:
        return intent
    return {"action": "unknown", "target": None}

def detect_intent(command: str):
    return get_intent(command)
