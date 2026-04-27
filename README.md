# CLI Text Analyzer

CLI Text Analyzer is a small Python command-line tool that reads plain-text files and prints a handful of useful statistics. It was built for my IS 4010 final project as a focused example of a program that solves one problem clearly instead of trying to do too much.

The tool reports word count, sentence count, average word length, average sentence length, common words, and a basic reading difficulty label. It also supports optional keyword counting, which makes it useful for quick analysis of essays, notes, reports, or other text files.

## What it does

- Counts words in a text file
- Counts sentences
- Calculates average word length
- Calculates average sentence length
- Shows the most common non-trivial words
- Counts specific keywords when requested
- Handles missing files and bad input without crashing

## Installation

1. Clone the repository:

```bash
git clone <your-github-repo-url>
cd is4010-text-analyzer
```

2. Make sure Python 3.11+ is installed:

```bash
python3 --version
```

3. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install the test dependency:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Usage

Run the analyzer with:

```bash
python3 main.py analyze <path-to-text-file>
```

Example:

```bash
python3 main.py analyze sample_texts/essay.txt
```

Expected output:

```text
Words: 31
Sentences: 3
Average word length: 5.03 characters
Average sentence length: 10.33 words
Top words: data (1), helps (1), business (1), make (1), better (1)
Reading difficulty: moderate
```

## Examples

Analyze a file and show the default top five words:

```bash
python3 main.py analyze sample_texts/essay.txt
```

Analyze a file and only show the top three words:

```bash
python3 main.py analyze sample_texts/essay.txt --top 3
```

Analyze a file and count keywords:

```bash
python3 main.py analyze sample_texts/essay.txt --keyword data --keyword users
```

Read from standard input:

```bash
echo "Data helps people. Data helps teams." | python3 main.py analyze -
```

## Testing

Run the test suite with:

```bash
python3 -m pytest
```

The project includes seven tests that cover core behavior like tokenizing text, counting sentences, ranking common words, keyword matching, difficulty labels, and empty input.

## Known limitations / future ideas

- Sentence detection is rule-based and not perfect for abbreviations
- Reading difficulty is a simple estimate, not a full academic formula
- A future version could export results to JSON or CSV
- A future version could support batch analysis for multiple files
