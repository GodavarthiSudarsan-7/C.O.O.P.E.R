import random

ACKS = [
    "Alright.",
    "On it.",
    "Understood.",
    "Right away.",
    "Okay."
]

DONE = [
    "Done.",
    "Completed.",
    "Task finished."
]

CONFIRM_POWER = [
    "This is a critical action. Do you want me to proceed?",
    "Please confirm before I continue.",
    "Are you sure you want to do that?"
]

UNKNOWN = [
    "I’m not sure about that.",
    "I didn’t fully understand.",
    "Could you please rephrase?"
]


def acknowledge():
    return random.choice(ACKS)


def done():
    return random.choice(DONE)


def confirm_power():
    return random.choice(CONFIRM_POWER)


def unknown():
    return random.choice(UNKNOWN)
