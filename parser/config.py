"""Environment and runtime configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass


TRUE_VALUES = {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Application settings sourced from environment variables."""

    log_level: str = "INFO"
    use_llm: bool = False
    llm_provider: str = "none"
    max_upload_mb: int = 10


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in TRUE_VALUES


def get_settings() -> Settings:
    """Build settings from environment variables."""

    return Settings(
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        use_llm=_env_bool("RESUME_PARSER_USE_LLM", False),
        llm_provider=os.getenv("RESUME_PARSER_LLM_PROVIDER", "none").lower(),
        max_upload_mb=int(os.getenv("RESUME_PARSER_MAX_UPLOAD_MB", "10")),
    )
