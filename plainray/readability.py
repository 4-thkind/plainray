"""Tiny Flesch-Kincaid grade-level calculator (stdlib only).

Used to show the reading-grade drop from the raw report to the explainer -
the concrete proof that "plain language" actually happened.
"""

import re

__all__ = ["fkgl_grade"]

_SENT_SPLIT = re.compile(r"[.!?]+")
_RAW_SENT = re.compile(r"[.!?][^.!?]*")
_WORD = re.compile(r"[A-Za-z][A-Za-z']*+")
_VOWELS = "aeiouyAEIOUY"


def _syllables(word: str) -> int:
    cleaned = re.sub(r"[^A-Za-z]", "", word).lower()
    if not cleaned:
        return 0
    count, prev_vowel = 0, False
    for ch in cleaned:
        is_vowel = ch in _VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if cleaned.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def fkgl_grade(text: str) -> float:
    """Flesch-Kincaid Grade Level for a block of text."""
    text = text.strip()
    if not text:
        return 0.0
    sentences = max(len(_RAW_SENT.findall(text)) or 1, 1)
    words = _WORD.findall(text)
    if not words:
        return 0.0
    syllables = sum(_syllables(w) for w in words)
    # FKGL = 0.39*(words/sent) + 11.8*(syl/words) - 15.59
    return 0.39 * (len(words) / sentences) + 11.8 * (syllables / len(words)) - 15.59
