"""Custom exceptions for the resume parser."""


class ResumeParserError(Exception):
    """Base exception for parser failures."""


class UnsupportedFileTypeError(ResumeParserError):
    """Raised when an input file extension is not supported."""


class DocumentLoadError(ResumeParserError):
    """Raised when text cannot be extracted from a supported document."""


class ExtractionError(ResumeParserError):
    """Raised when resume extraction cannot be completed."""
