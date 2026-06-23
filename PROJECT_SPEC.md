# Resume Parser Agent MVP

## Objective

Parse PDF and DOCX resumes and return structured JSON.

## Required Fields

- name
- email
- phone
- skills
- work_experience
- education

## Input Formats

- PDF
- DOCX
- TXT

## Output

Valid JSON matching a Pydantic schema.

## Interfaces

- Streamlit Web UI
- CLI

## Quality Requirements

- Modular architecture
- Type hints
- Logging
- Error handling
- Unit tests
- README
- Sample files

## Deployment

- Local execution
- Hugging Face Spaces compatible

## Future Extensibility

- LLM extraction providers
- OpenAI
- Anthropic
- Ollama
- RAG
- API endpoints
