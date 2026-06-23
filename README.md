# AI Resume Parser Agent

A production-quality but lightweight MVP that extracts structured JSON from PDF, DOCX, and TXT resumes. It is rule-based by default, requires no paid API, uses no database or authentication, and is compatible with free-tier deployments such as Hugging Face Spaces.

## Features

- Streamlit upload UI (`app.py`)
- Command-line parser (`cli.py`)
- PDF, DOCX, and TXT text extraction
- Rule-based extraction of:
  - name
  - email
  - phone
  - skills
  - work experience
  - education
- Pydantic-validated JSON output
- Optional LLM provider abstraction, disabled by default
- Pytest coverage and sample files

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the CLI:

```bash
python cli.py samples/sample_resume.txt
```

Run tests:

```bash
pytest
```

Run the web UI:

```bash
streamlit run app.py
```

## Configuration

Copy `.env.example` to `.env` if you want to customize environment variables:

```bash
cp .env.example .env
```

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `RESUME_PARSER_USE_LLM` | `false` | Reserved flag for future LLM extraction |
| `RESUME_PARSER_LLM_PROVIDER` | `none` | Optional provider name placeholder |
| `RESUME_PARSER_MAX_UPLOAD_MB` | `10` | Streamlit upload size guard |

## Project structure

```text
app.py                    # Streamlit UI
cli.py                    # CLI entry point
parser/config.py          # Environment settings
parser/document_loader.py # PDF, DOCX, TXT text extraction
parser/errors.py          # Custom exceptions
parser/extractor.py       # Rule-based extraction and LLM interface
parser/schema.py          # Pydantic models
samples/                  # Example input and output
tests/                    # Pytest suite
```

## Hugging Face Spaces

Create a Streamlit Space, upload this repository, and set the Space SDK to Streamlit. Hugging Face Spaces will install `requirements.txt` and run the Streamlit app.

## Notes and limitations

Rule-based resume parsing is intentionally lightweight and deterministic. It works best with resumes that use recognizable headings such as `Skills`, `Work Experience`, and `Education`. The `LLMProvider` interface in `parser/extractor.py` is included for future OpenAI, Anthropic, Ollama, or RAG integrations without making any paid provider mandatory.
