# Sandevistan

AI-powered CLI tool that analyzes Apple IPS crash files using LangGraph and Google Gemini Flash.

## Installation

### Option 1: Homebrew (macOS)
```bash
brew tap Dil4rd/sandevistan
brew install sandevistan
```

### Option 2: uvx (fast, cross-platform)
```bash
# Install from PyPI (when published)
uvx sandevistan

# Or run locally without installation
uvx --from . sandy --help
```

### Option 3: pipx
```bash
pipx install sandevistan
```

### Option 4: Development mode
```bash
uv pip install -e .
```

## Setup

1. Configure your Google API key:
```bash
sandy config --api-key YOUR_KEY
```

Get your API key at: https://makersuite.google.com/app/apikey

## Usage

### Analyze crash files
```bash
sandy analyze <path/to/crash/folder>
```

Example:
```bash
sandy analyze ~/Library/Logs/DiagnosticReports/
```

### Configuration commands
```bash
sandy config --show                # Display current config
sandy config --path                # Show config file location
sandy config --api-key YOUR_KEY    # Set/update API key
```

## How it works

Sandevistan will:
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
