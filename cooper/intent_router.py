from cooper.intent_rules import rule_intent
from cooper.intent_ai import ai_intent


def get_intent(command: str):
    
    intent = rule_intent(command)
    if intent:
        return intent

    
    return ai_intent(command)
