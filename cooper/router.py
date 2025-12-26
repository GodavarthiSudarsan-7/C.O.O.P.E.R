def route(user_input: str) -> str:
    """
    Decide whether the input is an ACTION or just THINKING.
    """
    user_input = user_input.lower().strip()

    # Action-based commands
    action_keywords = (
        "open",
        "run",
        "start",
        "launch",
    )

    for word in action_keywords:
        if user_input.startswith(word):
            return "ACTION"

    return "THINK"
