# AI_Agent

AI_Agent is a small learning project built as part of the [Boot.dev](https://www.boot.dev/) AI Agent course. It is a command-line Python program that connects to Google's Gemini API and lets the model call a few local helper functions.

The code is intentionally experimental and a little all over the place because the project was used for learning, practicing function calling, and understanding how an AI coding agent can inspect and modify files. It is not meant to be a polished, production-ready tool.

## What the program does

The main program in `main.py` starts a CLI chatbot. It takes a user prompt from the command line, sends it to Gemini, and allows Gemini to call a small set of local tools:

- list files and directories
- read file contents
- write or overwrite files
- run Python files with optional arguments

The agent uses function declarations from the Google GenAI SDK and routes model-requested function calls through `functions/call_function.py`.

For safety, the helper functions are currently scoped to the `./calculator` directory. This means the agent is mainly expected to inspect, edit, and run the included calculator demo project rather than the whole repository.

## Project structure

```text
AI_Agent/
├── main.py                         # CLI entry point for the AI agent
├── prompts.py                      # System prompt for the agent
├── pyproject.toml                  # Python project metadata and dependencies
├── uv.lock                         # Locked dependency versions
├── .python-version                 # Python version used for the project
├── .gitignore                      # Ignores env files, caches, build outputs, and virtualenvs
├── functions/
│   ├── call_function.py            # Dispatches model function calls
│   ├── get_files_info.py           # Lists files in the permitted working directory
│   ├── get_files_content.py        # Reads file contents with a size limit
│   ├── run_python_file.py          # Runs Python files in the permitted working directory
│   └── write_file.py               # Writes or overwrites files in the permitted working directory
└── calculator/
    ├── main.py                     # Demo calculator application
    ├── tests.py                    # Unit tests for the calculator
    └── pkg/
        ├── calculator.py           # Calculator logic
        └── render.py               # JSON output formatting
```

## How it works

1. `main.py` loads `GEMINI_API_KEY` from the environment using `python-dotenv`.
2. The user prompt is read from the command line.
3. Gemini receives the prompt together with the system instruction from `prompts.py`.
4. If Gemini asks to call a tool, `functions/call_function.py` dispatches that request to the correct helper function.
5. The helper result is sent back into the conversation loop.
6. The loop continues until Gemini returns a normal text response or the maximum iteration limit is reached.

The included `calculator/` directory acts as a safe-ish sandbox target for the agent. The calculator itself can evaluate simple space-separated arithmetic expressions, for example:

```bash
python calculator/main.py "3 * 4 + 5"
```

## Requirements

This project uses Python 3.13.

Dependencies are defined in `pyproject.toml`:

- `google-genai==1.12.1`
- `python-dotenv==1.1.0`

## Setup

Using `uv`:

```bash
uv sync
```

Create a local `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the agent with a prompt:

```bash
uv run python main.py "inspect the calculator project and explain what it does"
```

With verbose output:

```bash
uv run python main.py "run the calculator tests" --verbose
```

## Important safety warning

This project should not be used as a real coding assistant without extra safeguards.

The agent can:

- read files inside the configured working directory
- overwrite files inside the configured working directory
- execute Python files inside the configured working directory

Even though the current implementation restricts tool access to `./calculator`, running model-generated tool calls is still risky. Do not run this on important files, private data, production code, or untrusted repositories unless you fully understand the risks.

Possible risks include:

- accidental file overwrites
- execution of unsafe Python code
- leaking file contents into an AI model request
- unexpected changes caused by unclear prompts
- poor reliability because the project is still a learning exercise

Use this only in a disposable learning environment.

## Sensitive files / cleanup notes

A quick repository review did not show an uploaded `.env` file, and `.gitignore` correctly excludes `.env`, `.venv`, Python cache files, and build artifacts.

Files that are okay to keep:

- `pyproject.toml` because it documents the project dependencies
- `uv.lock` because it makes dependency installs reproducible
- `.python-version` because it records the Python version
- `calculator/` because it is the Boot.dev demo target used by the agent

Things to double-check before making the repository public:

- make sure no `.env` file or API key was ever committed in the Git history
- make sure no personal notes, real credentials, or private test data are added later
- consider adding stronger sandboxing before using the agent on any real project

## Status

This repository is a Boot.dev learning project, not a finished product. The code works as a practice implementation of an AI function-calling agent, but it is intentionally rough and should be treated as educational material only.
