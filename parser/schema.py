"""Pydantic schemas for validated resume parser output."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class WorkExperience(BaseModel):
    """A lightweight work history item."""

    company: str | None = None
    title: str | None = None
    dates: str | None = None
    description: str | None = None


class Education(BaseModel):
    """A lightweight education item."""

    institution: str | None = None
    degree: str | None = None
    dates: str | None = None
    description: str | None = None


class Resume(BaseModel):
    """Validated structured resume output."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    skills: list[str] = Field(default_factory=list)
    work_experience: list[WorkExperience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)

    @field_validator("skills")
    @classmethod
    def normalize_skills(cls, skills: list[str]) -> list[str]:
        """Deduplicate skills while preserving first-seen order."""

        seen: set[str] = set()
        normalized: list[str] = []
        for skill in skills:
            clean = " ".join(skill.strip().split())
            key = clean.lower()
            if clean and key not in seen:
                normalized.append(clean)
                seen.add(key)
        return normalized

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize the resume as JSON."""

        return self.model_dump_json(indent=indent)


def parse_resume_json(data: str | dict[str, Any]) -> Resume:
    """Validate a JSON string or dictionary as a Resume."""

    if isinstance(data, str):
        return Resume.model_validate(json.loads(data))
    return Resume.model_validate(data)
