"""Command-line interface for the Resume Parser Agent."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from parser.config import get_settings
from parser.document_loader import load_document
from parser.errors import ResumeParserError
from parser.extractor import ResumeExtractor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse a resume file and print validated JSON.")
    parser.add_argument("path", type=Path, help="Path to a PDF, DOCX, or TXT resume")
    parser.add_argument("--output", "-o", type=Path, help="Optional JSON output file")
    return parser


def main(argv: list[str] | None = None) -> int:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(levelname)s:%(name)s:%(message)s")
    args = build_parser().parse_args(argv)

    try:
        text = load_document(args.path)
        resume = ResumeExtractor(use_llm=settings.use_llm).extract(text)
        output = resume.to_json()
        if args.output:
            args.output.write_text(output + "\n", encoding="utf-8")
        print(output)
        return 0
    except ResumeParserError as exc:
        logging.getLogger(__name__).error("%s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
