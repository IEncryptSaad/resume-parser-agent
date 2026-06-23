"""Streamlit web UI for the Resume Parser Agent."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import streamlit as st

from parser.config import get_settings
from parser.document_loader import SUPPORTED_EXTENSIONS, load_document
from parser.errors import ResumeParserError
from parser.extractor import ResumeExtractor

settings = get_settings()
logging.basicConfig(level=settings.log_level, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Resume Parser Agent", page_icon="📄", layout="centered")
st.title("📄 AI Resume Parser Agent")
st.caption("Free, lightweight, rule-based resume parsing for PDF, DOCX, and TXT files.")

uploaded = st.file_uploader("Upload a resume", type=[ext.lstrip(".") for ext in sorted(SUPPORTED_EXTENSIONS)])

if uploaded is None:
    st.info("Upload a PDF, DOCX, or TXT resume to generate validated JSON.")
else:
    suffix = Path(uploaded.name).suffix.lower()
    if uploaded.size > settings.max_upload_mb * 1024 * 1024:
        st.error(f"File is larger than the configured {settings.max_upload_mb} MB limit.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.getbuffer())
            tmp_path = Path(tmp.name)
        try:
            text = load_document(tmp_path)
            resume = ResumeExtractor(use_llm=False).extract(text)
            st.success("Resume parsed successfully.")
            st.subheader("Extracted JSON")
            st.json(resume.model_dump(mode="json"))
            st.download_button(
                "Download JSON",
                resume.to_json(),
                file_name=f"{Path(uploaded.name).stem}_parsed.json",
                mime="application/json",
            )
        except ResumeParserError as exc:
            logger.exception("Resume parsing failed")
            st.error(str(exc))
        finally:
            tmp_path.unlink(missing_ok=True)
