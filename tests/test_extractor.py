from pathlib import Path

from parser.document_loader import load_document
from parser.extractor import ResumeExtractor
from parser.schema import Resume, parse_resume_json


def test_extract_sample_resume() -> None:
    text = load_document(Path("samples/sample_resume.txt"))
    resume = ResumeExtractor().extract(text)

    assert isinstance(resume, Resume)
    assert resume.name == "Jane Doe"
    assert resume.email == "jane.doe@example.com"
    assert resume.phone == "(555) 123-4567"
    assert "python" in [skill.lower() for skill in resume.skills]
    assert resume.work_experience[0].company == "Acme Analytics"
    assert resume.education[0].institution == "Bachelor of Science in Computer Science, State University"


def test_resume_json_round_trip() -> None:
    text = load_document(Path("samples/sample_resume.txt"))
    resume = ResumeExtractor().extract(text)
    reparsed = parse_resume_json(resume.to_json())
    assert reparsed == resume


def test_presentation_designer_does_not_match_present_date_token() -> None:
    resume = ResumeExtractor().extract(
        "John Smith\n"
        "Experience\n"
        "Presentation Designer at Acme | 2020 - 2024\n"
    )

    assert resume.work_experience[0].title == "Presentation Designer"
    assert resume.work_experience[0].company == "Acme"
    assert resume.work_experience[0].dates == "2020 - 2024"
