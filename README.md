<p align="center">
  <img src="logo.png" alt="Deckard Logo" width="200"/>
</p>

# Deckard

AI-powered CLI tool that analyzes Apple IPS crash files using LangGraph and Google Gemini Flash.

## Quick Start

### Install with uvx (recommended - fast!)
```bash
uvx --from . deckard --help
```

### Or install in development mode
```bash
uv pip install -e .
deckard --help
```

## Setup

1. Configure your Google API key:
```bash
deckard config --api-key YOUR_KEY
```

Get your API key at: https://makersuite.google.com/app/apikey

## Usage

### Analyze crash files
```bash
deckard analyze <path/to/crash/folder>
```

Example:
```bash
deckard analyze ~/Library/Logs/DiagnosticReports/
```

### Configuration commands
```bash
deckard config --show                # Display current config
deckard config --path                # Show config file location
deckard config --api-key YOUR_KEY    # Set/update API key
```

## How it works

Deckard will:
1. Scan the specified folder for `.ips` files
2. Analyze each crash file using Google Gemini Flash
3. Output plain-language explanations including:
   - What crashed
   - Why it crashed (root cause)
   - Key technical details

## Requirements

- Python 3.11+
- Google API key
- `uv` package manager (install from https://github.com/astral-sh/uv)
