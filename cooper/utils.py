def clean_input(text: str) -> str:
    return text.strip()


def normalize_command(text: str) -> str:
    """
    Fix common speech-to-text mistakes.
    """
    corrections = {
        "open your dube": "open youtube",
        "open you dube": "open youtube",
        "open you tube": "open youtube",
        "open gugel": "open google",
        "open gogle": "open google",
        "hey coop": "hey cooper",
        "hey cooper.": "hey cooper",
        "open your tube": "open youtube",
    }

    text = text.lower().strip()

    for wrong, right in corrections.items():
        if wrong in text:
            return right

    return text
