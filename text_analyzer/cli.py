from __future__ import annotations

import argparse
import sys
from pathlib import Path

from text_analyzer.analyzer import analyze_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read a text file and print a few useful stats."
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a text file or stdin."
    )
    analyze_parser.add_argument(
        "path",
        help="Path to a text file. Use - to read from stdin.",
    )
    analyze_parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="How many top words to show. Default is 5.",
    )
    analyze_parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Keyword to count. Can be used more than once.",
    )

    return parser


def read_text(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()

    path = Path(path_arg)
    return path.read_text(encoding="utf-8")


def format_report(result: dict[str, object]) -> str:
    top_words = result["top_words"]
    top_word_text = ", ".join(f"{word} ({count})" for word, count in top_words)
    if not top_word_text:
        top_word_text = "None"

    lines = [
        f"Words: {result['word_count']}",
        f"Sentences: {result['sentence_count']}",
        f"Average word length: {result['average_word_length']:.2f} characters",
        f"Average sentence length: {result['average_sentence_length']:.2f} words",
        f"Top words: {top_word_text}",
        f"Reading difficulty: {result['reading_difficulty']}",
    ]

    keyword_counts = result.get("keyword_counts")
    if keyword_counts:
        lines.append("Keyword counts:")
        for keyword, count in keyword_counts.items():
            lines.append(f"  {keyword}: {count}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "analyze":
        parser.print_help()
        return 1

    if args.top < 1:
        print("error: --top must be at least 1", file=sys.stderr)
        return 1

    try:
        text = read_text(args.path)
    except FileNotFoundError:
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: could not read {args.path}: {exc}", file=sys.stderr)
        return 1

    result = analyze_text(text, top_n=args.top, keywords=args.keyword)
    print(format_report(result))
    return 0
