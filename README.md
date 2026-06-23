# AI Resume Parser Agent

## Project overview

AI Resume Parser Agent is a lightweight demo-ready resume parsing project that converts PDF, DOCX, and TXT resumes into structured, validated JSON. The parser is deterministic and rule-based by default, so it does not require paid AI APIs, background services, a database, or authentication. The project includes both a Streamlit web app and a command-line interface for quick local demos and Hugging Face Spaces deployment.

## Features

- Upload-based Streamlit app in `app.py`.
- Command-line parser in `cli.py`.
- PDF, DOCX, and TXT resume text extraction.
- Rule-based extraction for name, email, phone, skills, work experience, and education.
- Pydantic validation for structured JSON output.
- JSON download from the Streamlit UI.
- Clear parser errors for unsupported files, empty documents, and extraction failures.
- No paid API, database, or authentication required.
- Sample input and output files for demo validation.

## Local setup

Use Python 3.10 or newer. The commands below create an isolated environment and install the minimal dependencies needed to run the app, CLI, document loaders, and tests.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Optional environment variables are read directly from the environment; no `.env` file is required.

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Python logging level. |
| `RESUME_PARSER_USE_LLM` | `false` | Reserved switch for future optional LLM integrations; leave false for the free demo. |
| `RESUME_PARSER_LLM_PROVIDER` | `none` | Placeholder provider name for future extension. |
| `RESUME_PARSER_MAX_UPLOAD_MB` | `10` | Streamlit upload size guard in megabytes. |

## CLI usage

Parse the included sample resume and print validated JSON:

```bash
python cli.py samples/sample_resume.txt
```

Write JSON to a file as well as stdout:

```bash
python cli.py samples/sample_resume.txt --output parsed_resume.json
```

The CLI exits with status code `0` on success and `1` for known parser errors such as unsupported file types or unreadable documents.

## Streamlit usage

Start the local web demo:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit, upload a PDF, DOCX, or TXT resume, review the extracted JSON, and use the download button to save the result.

## Testing

Run the full test suite with:

```bash
pytest
```

For a quick manual smoke test, run:

```bash
python cli.py samples/sample_resume.txt
streamlit run app.py
```

## Hugging Face Spaces deployment

This project is compatible with the free Hugging Face Spaces Streamlit SDK.

1. Create a new Space on Hugging Face.
2. Select **Streamlit** as the Space SDK.
3. Choose the free CPU hardware tier.
4. Upload or push this repository to the Space.
5. Ensure the repository root contains `app.py` and `requirements.txt`.
6. Hugging Face Spaces will install `requirements.txt` and launch the Streamlit app automatically.
7. Open the Space URL and upload a sample PDF, DOCX, or TXT resume to confirm the demo.

No secrets are required for the default demo because the parser does not call paid APIs.

## Client-facing demo note

This demo accepts PDF, DOCX, and TXT resumes and returns structured JSON for the main candidate fields. Output is validated with Pydantic before display or download. The app provides user-friendly error messages for unsupported file types, oversized uploads, unreadable files, and empty content. The default workflow is fully rule-based and requires no paid API key.

## Limitations

- The parser is intentionally lightweight and does not redesign or replace the core rule-based extraction logic.
- Accuracy depends on resume formatting and recognizable headings such as `Skills`, `Experience`, and `Education`.
- Scanned image-only PDFs are not OCRed.
- Highly stylized multi-column resumes may produce partial text extraction depending on PDF/DOCX structure.
- The optional LLM provider interface is a future extension point only; no paid provider is required or configured for this demo.

## Project structure

```text
app.py                    # Streamlit UI
cli.py                    # CLI entry point
parser/config.py          # Environment settings
parser/document_loader.py # PDF, DOCX, TXT text extraction
parser/errors.py          # Custom exceptions
parser/extractor.py       # Rule-based extraction and optional LLM interface
parser/schema.py          # Pydantic models
samples/                  # Example input and output
tests/                    # Pytest suite
```
