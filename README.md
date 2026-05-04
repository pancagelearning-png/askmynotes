---
title: AskMyNotes
emoji: 📚
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 3.50.2
app_file: app.py
pinned: false
---

# AskMyNotes

AskMyNotes lets you chat with your own notes and PDFs using AI. Ask questions in plain English and get answers sourced directly from your documents.

> **Note:** The `chroma_db/` vector database is rebuilt automatically on every startup from the files in `notes/`.

## Run locally

```bash
pip install -r requirements.txt
python3 app.py
```

Open your browser at http://localhost:7860

## Environment variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key (required) |
