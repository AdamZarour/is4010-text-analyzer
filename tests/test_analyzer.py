from text_analyzer.analyzer import (
    analyze_text,
    classify_reading_difficulty,
    extract_sentences,
    extract_words,
    get_keyword_counts,
    get_top_words,
)


def test_extract_words_handles_case_and_punctuation():
    text = "Data, data, and more DATA. User-friendly tools help."
    assert extract_words(text) == [
        "data",
        "data",
        "and",
        "more",
        "data",
        "user",
        "friendly",
        "tools",
        "help",
    ]


def test_extract_sentences_splits_on_common_end_marks():
    text = "One sentence. Another one! Last one?"
    assert extract_sentences(text) == [
        "One sentence",
        "Another one",
        "Last one",
    ]


def test_get_top_words_filters_common_words():
    words = ["the", "data", "data", "system", "user", "system", "and"]
    assert get_top_words(words, limit=3) == [
        ("data", 2),
        ("system", 2),
        ("user", 1),
    ]


def test_keyword_counts_are_case_insensitive():
    words = extract_words("Data drives better data decisions for every user.")
    assert get_keyword_counts(words, ["Data", "user", "missing"]) == {
        "data": 2,
        "user": 1,
        "missing": 0,
    }


def test_analyze_text_returns_core_stats():
    text = "Business data helps every user. Good systems save time."
    result = analyze_text(text, top_n=2, keywords=["data", "user"])

    assert result["word_count"] == 9
    assert result["sentence_count"] == 2
    assert result["average_sentence_length"] == 4.5
    assert result["top_words"] == [("business", 1), ("data", 1)]
    assert result["keyword_counts"] == {"data": 1, "user": 1}


def test_empty_text_is_handled_cleanly():
    result = analyze_text("")
    assert result["word_count"] == 0
    assert result["sentence_count"] == 0
    assert result["average_word_length"] == 0.0
    assert result["reading_difficulty"] == "very easy"


def test_classify_reading_difficulty_uses_simple_bands():
    assert classify_reading_difficulty(8, 4.2) == "easy"
    assert classify_reading_difficulty(16, 5.0) == "moderate"
    assert classify_reading_difficulty(24, 6.1) == "hard"
