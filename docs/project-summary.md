# Project Summary: notebooklm-py

`notebooklm-py` is a comprehensive, unofficial Python API and command-line interface (CLI) for Google NotebookLM. It provides full programmatic access to NotebookLM's capabilities, including many features that are not exposed in the standard web interface.

## 🚀 Core Value Proposition

- **Programmatic Control**: Automate research, content generation, and artifact management.
- **Agent Integration**: Built-in support for AI agents (Claude Code, Codex) via skills and specialized instructions.
- **Beyond Web UI**: Access advanced features like batch downloads, slide revisions, and structured data exports (JSON, CSV, Markdown).
- **Automation Ready**: Designed for CI/CD, headless environments, and bulk processing.

## 🛠️ Key Capabilities

### 1. Notebook & Source Management
- **Full CRUD**: Create, list, rename, and delete notebooks.
- **Diverse Sources**: Support for URLs, YouTube videos, local files (PDF, TXT, MD, DOCX, etc.), Google Drive, and pasted text.
- **Source Insights**: Retrieve full indexed text, source guides, and citations.

### 2. Intelligent Chat & Research
- **Contextual Q&A**: Ask questions across all sources or specific subsets.
- **Citations**: Detailed references to source text in chat answers.
- **Research Agents**: Fast and Deep research modes with automated source importing.
- **Note Management**: Save chat responses or full histories as notebook notes.

### 3. Advanced Content Generation
Generate a wide variety of artifacts with granular control:
- **Audio Overviews**: Multiple formats (podcast, critique, etc.), lengths, and 50+ languages.
- **Video Overviews**: Visual styles including cinematic and whiteboard modes.
- **Slide Decks**: Detailed or presenter formats with individual slide revision support.
- **Interactive Study Tools**: Quizzes and Flashcards with configurable difficulty.
- **Visuals & Data**: Infographics (PNG), Mind Maps (JSON), and Data Tables (CSV).

## 🌍 Integration Ecosystem

| Method | Description |
| :--- | :--- |
| **Python API** | Asyncio-based client for deep application integration. |
| **CLI** | Powerful command-line tool with 30+ commands and `--json` support. |
| **Agent Skills** | Native skills for **Claude Code** and **Codex** (`AGENTS.md`, `SKILL.md`). |

## 🏗️ Technical Architecture

- **Core Logic**: RPC-based communication with undocumented Google endpoints (`src/notebooklm/rpc/`).
- **Client**: `NotebookLMClient` provides the main async entry point.
- **Storage**: Configurable local storage for cookies and settings, supporting `NOTEBOOKLM_HOME`.
- **Authentication**: Browser-based login using Playwright for robust session management.
- **Diagnostics**: Built-in `doctor` and `auth check` commands for troubleshooting.

## 📈 Project Guidelines (for Developers)

- **Language**: Python 3.10+
- **Tooling**: `uv` for dependency management, `ruff` for linting/formatting.
- **Testing**: Triple-layered testing strategy (Unit, Integration with VCR, and E2E).
- **Stability**: Follows Semantic Versioning; internal modules prefixed with `_`.

---
*For more details, see the [CLI Reference](cli-reference.md) or [Python API Documentation](python-api.md).*
