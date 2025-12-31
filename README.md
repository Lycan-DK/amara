# AMARA

AMARA is a lightweight **Streamlit** chat app designed to support caregivers with quick, context-aware responses.

It uses an OpenAI Chat model (fine-tuned model ID configured in `app.py`) and a simple rules layer that enriches user prompts with caregiver-relevant context.

## What it does

- Provides a clean chat UI (Streamlit)
- Stores conversation history in Streamlit session state
- Sends your prompt + conversation context to the configured OpenAI model
- Adds small context hints (demo logic) such as:
	- user mentioned in the prompt → append health context (e.g., diabetes / heart condition)
	- limits responses to ~300 characters for concise guidance

## Tech stack

- Python
- Streamlit
- OpenAI Python SDK

## Project structure

```
amara/
	app.py
	requirements.txt
	README.md
	fine-tune.jsonl
	train-new.jsonl
```

## Setup

### 1) Create a virtual environment (recommended)

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

## Configuration

### OpenAI API key

Set your OpenAI API key using **one** of the options below.

#### Option A: Environment variable (recommended)

```powershell
$env:OPENAI_API_KEY = "YOUR_API_KEY"
```

#### Option B: Streamlit secrets

Create a file `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "YOUR_API_KEY"
```

> Note: Don’t commit API keys to git.

## Run the app

```powershell
streamlit run app.py
```

The app will start locally and open in your browser.

## Troubleshooting

- **Blank/failed responses**: confirm `OPENAI_API_KEY` is set.
- **Import errors**: re-run `pip install -r requirements.txt` inside your venv.
- **Model access errors**: ensure the model ID in `app.py` exists for your OpenAI account.

## Notes for improvement (optional)

- Move user context rules (diabetes/heart) into a config file instead of hard-coding.
- Add a "Clear conversation" button (sidebar) and token/cost reporting UI.
- Add basic input validation and a safer medical disclaimer if needed.