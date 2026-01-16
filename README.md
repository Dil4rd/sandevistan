# ⚡ Sandevistan

> **AI-augmented Apple security research toolkit**

Sandevistan augments your security research with AI-powered tools for analyzing Apple crash reports, tracking security updates, and more.

```bash
sandy analyze crash.ips      # AI-powered crash analysis
sandy scrape                 # Fetch Apple security updates
# ✨ Powered by Google Gemini Flash
```

---

## 🎯 Why Sandevistan?

Like the Cyberpunk cyberware it's named after, Sandevistan augments your capabilities—letting you process security data at machine speed.

| Challenge | How Sandevistan Helps |
|-----------|----------------------|
| 😵 Crash logs are cryptic | 📖 AI translates IPS files to plain English |
| ⏰ Tracking updates is tedious | 🔄 Auto-scrape Apple security advisories |
| 🤔 CVE details scattered | 📊 Structured data export (JSON/CSV/SQLite) |
| 📚 Need deep Apple internals knowledge | 🤖 AI handles the technical analysis |

---

## 🚀 Quick Start

### 📦 Installation

**macOS (Homebrew):**
```bash
brew tap Dil4rd/sandevistan
brew install sandevistan
```

**Cross-platform (uvx - recommended):**
```bash
uvx sandevistan  # or 'sandy' for short
```

**Alternative (pipx):**
```bash
pipx install sandevistan
```

### 🔑 Setup (one-time)

```bash
sandy config --api-key YOUR_GOOGLE_API_KEY
```

🔗 Get your free API key: [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 🔧 Features

> **Note:** Both `sandevistan` and `sandy` commands work identically. Examples below use `sandy` for brevity.

### 🧠 Crash Analysis

Analyze Apple IPS crash files with AI-powered explanations.

```bash
# Single file
sandy analyze crash.ips

# Entire folder
sandy analyze ~/Library/Logs/DiagnosticReports/
```

When multiple files are found, you'll get an interactive menu:
```
Found 3 IPS files in ./crashes:
  [0] All files
  [1] AppCrash_2024-01-15.ips
  [2] KernelPanic_2024-01-16.ips
  [3] SegFault_2024-01-17.ips

Select files to analyze (e.g., "1,3" or "0" for all): _
```

**What you get:**
- ✅ **What crashed** — Process, thread, and component that failed
- ✅ **Why it crashed** — Root cause in plain English
- ✅ **Key details** — Exception types, addresses, and code symbols

### 🔍 Security Updates Scraper

Scrape Apple's security updates and CVE data into structured formats.

```bash
# Scrape to all formats (JSON, CSV, SQLite)
sandy scrape

# Specific format(s)
sandy scrape -f json
sandy scrape -f json -f csv

# Custom output filename
sandy scrape -o security_updates

# Fast mode (skip detailed CVE scraping)
sandy scrape --skip-advisories
```

**Output includes:**
- 📋 Security update metadata (date, OS, version, URL)
- 🐛 CVE entries with descriptions
- 🔗 Links to full advisories

### ⚙️ Configuration

```bash
sandy config --show                # 📋 View current settings
sandy config --path                # 📂 Show config location
sandy config --api-key YOUR_KEY    # 🔐 Update API key
sandy config --model gemini-2.0    # 🤖 Change AI model
sandy config --delay 2.0           # ⏱️ Set scraper rate limit
```

---

## 📝 Example Output

### Crash Analysis
```
Analyzing file: MyApp_2024-01-15.ips
Using model: gemini-2.0-flash-exp
────────────────────────────────────────────────────────────────────────────────

**What crashed:** MyApp (process) crashed in the main thread

**Why it crashed:** Null pointer dereference - The app attempted to access
memory at address 0x0, which is not a valid memory location.

**Key technical details:**
- Exception Type: EXC_BAD_ACCESS (SIGSEGV)
- Exception Codes: KERN_INVALID_ADDRESS at 0x0000000000000000
- Crashed Thread: 0 (Main thread)
- Relevant Frame: MyApp`-[MyViewController buttonTapped:] + 42
```

### Security Updates Scrape
```
Scraping Apple security updates...
Found 156 security updates
Fetching advisory details... [████████████████████] 100%
Exported to: security_updates.json, security_updates.csv, security_updates.db
```

---

## 🛠️ Development

### Local development
```bash
# Clone the repo
git clone https://github.com/Dil4rd/sandevistan.git
cd sandevistan

# Run without installation
uvx --from . sandy --help

# Install in editable mode
uv pip install -e .
```

### Requirements
- 🐍 Python 3.11+
- 🔑 Google API key (free tier available)
- 📦 `uv` package manager ([install here](https://github.com/astral-sh/uv))

---

## 🏗️ Architecture

Built with modern Python tools for speed and reliability:

- **🧠 AI Engine:** Google Gemini Flash (fast, accurate analysis)
- **🔄 Workflow:** LangGraph (structured multi-step pipelines)
- **⚙️ CLI:** Click (user-friendly command interface)
- **📦 Package Manager:** uv (blazing fast dependency resolution)

---

## 🗺️ Roadmap

Future augmentations planned:

- [ ] IPS explannation caching for efficient token reuse
- [ ] IPS deduplication
- [ ] Incremental security updates scrape
- [ ] Advanced analytics of security udpates

---

## 🤝 Contributing

Found a bug? Have an idea? Contributions are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Package management by [uv](https://github.com/astral-sh/uv)

---

<div align="center">

**⚡ Augment your Apple security research**

[Get Started](#-quick-start) • [Report Bug](https://github.com/Dil4rd/sandevistan/issues) • [Request Feature](https://github.com/Dil4rd/sandevistan/issues)

</div>
