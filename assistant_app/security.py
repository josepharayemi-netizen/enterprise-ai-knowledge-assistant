import re

PATTERNS=[
    r"ignore (all |any )?previous instructions",
    r"reveal (the )?(system|developer) prompt",
    r"bypass (security|access|authorization)",
    r"send .* (secret|password|token)",
    r"act as (an? )?(administrator|root)",
]


def suspicious(text:str)->bool:
    lowered=text.lower()
    return any(re.search(pattern,lowered) for pattern in PATTERNS)
