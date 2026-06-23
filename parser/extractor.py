"""Rule-based resume extraction with an optional LLM-provider extension point."""

from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod

from parser.errors import ExtractionError
from parser.schema import Education, Resume, WorkExperience

logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4})")
DATE_RE = re.compile(
    r"(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+)?\d{4}\s*(?:-|–|to)\s*(?:(?:Present|Current)|(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+)?\d{4})|Present|Current",
    re.IGNORECASE,
)
SECTION_HEADERS = {
    "summary",
    "profile",
    "objective",
    "skills",
    "technical skills",
    "experience",
    "work experience",
    "professional experience",
    "employment",
    "education",
    "projects",
    "certifications",
}
DEFAULT_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "sql",
    "postgresql",
    "mysql",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "linux",
    "git",
    "react",
    "node.js",
    "django",
    "flask",
    "fastapi",
    "streamlit",
    "pandas",
    "numpy",
    "machine learning",
    "nlp",
    "etl",
    "excel",
    "tableau",
    "power bi",
    "project management",
    "agile",
    "scrum",
    "communication",
    "leadership",
}


class LLMProvider(ABC):
    """Optional extraction provider interface; disabled unless explicitly wired in."""

    @abstractmethod
    def extract(self, text: str) -> Resume:
        """Extract a resume from raw text."""


class ResumeExtractor:
    """Extract structured resume fields using deterministic rules by default."""

    def __init__(self, *, llm_provider: LLMProvider | None = None, use_llm: bool = False) -> None:
        self.llm_provider = llm_provider
        self.use_llm = use_llm

    def extract(self, text: str) -> Resume:
        """Return a validated Resume from raw resume text."""

        if not text or not text.strip():
            raise ExtractionError("Cannot extract resume fields from empty text.")
        if self.use_llm and self.llm_provider is not None:
            logger.info("Using configured LLM provider for extraction.")
            return self.llm_provider.extract(text)

        logger.info("Using rule-based resume extraction.")
        lines = _clean_lines(text)
        resume = Resume(
            name=self._extract_name(lines),
            email=self._first_match(EMAIL_RE, text),
            phone=self._first_match(PHONE_RE, text),
            skills=self._extract_skills(text),
            work_experience=self._extract_work_experience(lines),
            education=self._extract_education(lines),
        )
        return resume

    @staticmethod
    def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
        match = pattern.search(text)
        return match.group(0).strip() if match else None

    def _extract_name(self, lines: list[str]) -> str | None:
        for line in lines[:8]:
            lower = line.lower()
            if EMAIL_RE.search(line) or PHONE_RE.search(line) or lower in SECTION_HEADERS:
                continue
            if len(line.split()) in {2, 3, 4} and not any(char.isdigit() for char in line):
                if sum(1 for c in line if c.isalpha()) >= 4:
                    return line
        return None

    def _extract_skills(self, text: str) -> list[str]:
        lower_text = text.lower()
        skills = [skill for skill in sorted(DEFAULT_SKILLS) if re.search(rf"(?<![\w.+-]){re.escape(skill)}(?![\w.+-])", lower_text)]
        section = _section_text(_clean_lines(text), {"skills", "technical skills"})
        if section:
            for token in re.split(r"[,;|•\n]", section):
                clean = token.strip(" -\t")
                if 1 <= len(clean.split()) <= 4 and len(clean) <= 40:
                    skills.append(clean)
        return skills

    def _extract_work_experience(self, lines: list[str]) -> list[WorkExperience]:
        section_lines = _section_lines(lines, {"experience", "work experience", "professional experience", "employment"})
        items: list[WorkExperience] = []
        current: dict[str, str | None] | None = None
        descriptions: list[str] = []

        for line in section_lines:
            date = DATE_RE.search(line)
            looks_like_role = bool(date) or " at " in line.lower() or " - " in line or " | " in line
            if looks_like_role and not line.startswith(("-", "•")):
                if current:
                    current["description"] = " ".join(descriptions).strip() or None
                    items.append(WorkExperience(**current))
                current = self._parse_experience_line(line)
                descriptions = []
            elif current:
                descriptions.append(line.lstrip("-• "))
        if current:
            current["description"] = " ".join(descriptions).strip() or None
            items.append(WorkExperience(**current))
        return items[:5]

    def _parse_experience_line(self, line: str) -> dict[str, str | None]:
        dates = self._first_match(DATE_RE, line)
        clean = DATE_RE.sub("", line).strip(" -–|,")
        title: str | None = None
        company: str | None = None
        if " at " in clean.lower():
            parts = re.split(r"\s+at\s+", clean, maxsplit=1, flags=re.IGNORECASE)
            title, company = parts[0].strip(), parts[1].strip()
        elif " | " in clean:
            title, company = [p.strip() for p in clean.split(" | ", 1)]
        elif " - " in clean:
            title, company = [p.strip() for p in clean.split(" - ", 1)]
        else:
            title = clean or None
        return {"title": title, "company": company, "dates": dates, "description": None}

    def _extract_education(self, lines: list[str]) -> list[Education]:
        section_lines = _section_lines(lines, {"education"})
        items: list[Education] = []
        for line in section_lines:
            lower = line.lower()
            if any(word in lower for word in ("university", "college", "school", "institute", "bachelor", "master", "ph.d", "degree")):
                dates = self._first_match(DATE_RE, line)
                clean = DATE_RE.sub("", line).strip(" -–|,")
                items.append(Education(institution=clean or None, dates=dates, description=line))
        return items[:5]


def _clean_lines(text: str) -> list[str]:
    return [" ".join(line.strip().split()) for line in text.splitlines() if line.strip()]


def _is_header(line: str) -> bool:
    return line.strip().lower().rstrip(":") in SECTION_HEADERS


def _section_lines(lines: list[str], headers: set[str]) -> list[str]:
    selected: list[str] = []
    in_section = False
    for line in lines:
        normalized = line.lower().rstrip(":")
        if normalized in headers:
            in_section = True
            continue
        if in_section and _is_header(line):
            break
        if in_section:
            selected.append(line)
    return selected


def _section_text(lines: list[str], headers: set[str]) -> str:
    return "\n".join(_section_lines(lines, headers))
