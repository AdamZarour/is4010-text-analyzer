from __future__ import annotations

import re
from collections import Counter

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "can",
    "by",
    "every",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "more",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}


def extract_words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def extract_sentences(text: str) -> list[str]:
    pieces = SENTENCE_SPLIT_RE.split(text.strip())
    return [piece.strip() for piece in pieces if piece.strip()]


def get_top_words(words: list[str], limit: int = 5) -> list[tuple[str, int]]:
    filtered_words = [word for word in words if word not in STOP_WORDS]
    counts = Counter(filtered_words)
    return counts.most_common(limit)


def get_keyword_counts(words: list[str], keywords: list[str]) -> dict[str, int]:
    counts = Counter(words)
    return {keyword.lower(): counts[keyword.lower()] for keyword in keywords}


def classify_reading_difficulty(
    average_sentence_length: float, average_word_length: float
) -> str:
    if average_sentence_length == 0:
        return "very easy"
    if average_sentence_length < 12 and average_word_length < 5:
        return "easy"
    if average_sentence_length < 20 and average_word_length < 6:
        return "moderate"
    return "hard"


def analyze_text(
    text: str, *, top_n: int = 5, keywords: list[str] | None = None
) -> dict[str, object]:
    words = extract_words(text)
    sentences = extract_sentences(text)
    word_count = len(words)
    sentence_count = len(sentences)

    average_word_length = (
        sum(len(word) for word in words) / word_count if word_count else 0.0
    )
    average_sentence_length = (
        word_count / sentence_count if sentence_count else 0.0
    )

    result: dict[str, object] = {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_word_length": average_word_length,
        "average_sentence_length": average_sentence_length,
        "top_words": get_top_words(words, limit=top_n),
        "reading_difficulty": classify_reading_difficulty(
            average_sentence_length, average_word_length
        ),
    }

    if keywords:
        result["keyword_counts"] = get_keyword_counts(words, keywords)

    return result
