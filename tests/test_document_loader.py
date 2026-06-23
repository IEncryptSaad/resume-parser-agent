from pathlib import Path

import pytest

from parser.document_loader import load_document
from parser.errors import UnsupportedFileTypeError


def test_load_txt(tmp_path: Path) -> None:
    path = tmp_path / "resume.txt"
    path.write_text("Jane Doe\n", encoding="utf-8")
    assert load_document(path) == "Jane Doe\n"


def test_unsupported_file_type(tmp_path: Path) -> None:
    path = tmp_path / "resume.md"
    path.write_text("Jane", encoding="utf-8")
    with pytest.raises(UnsupportedFileTypeError):
        load_document(path)
