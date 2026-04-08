# Repo2Prompt

> **Convert any GitHub repository or local directory into a single text file properly formatted for large-context LLMs.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Context windows are huge now (Claude 3 has 200k, Gemini has 1M+). We all want to drop our *entire* codebase into an LLM to ask architecture questions, but copying file by file takes forever.

**Repo2Prompt** solves this by instantly analyzing a repository, strictly adhering to `.gitignore`, filtering out messy/compiled files, and building a visual representation arrayed alongside your beautifully clean code context.

## 🚀 Features

- **Zero API Keys Required**: Runs entirely locally.
- **Smart Filtering**: Automatically ignores `.git` histories, `node_modules`, `venv`, and huge lock files.
- **Auto `.gitignore` Matching**: Perfectly respects your project's `.gitignore` definitions thanks to `pathspec`.
- **Remote Git Support**: Provide any valid GitHub URL and it dynamically clones, parses, and cleans up after itself.
- **Visual File Tree**: Outputs a convenient, human-readable directory tree at the top of the context file so the LLM understands your routing and architecture before reading code.

## 📦 Installation

Clone this repository and install using pip:

```bash
git clone https://github.com/yourusername/repo2prompt.git
cd repo2prompt
pip install -e .
```

## 🛠 Usage

Once installed, simply run the CLI tool passing either a path or a remote Git URL:

```bash
# Analyze a local directory
repo2prompt .

# Analyze a remote repository (saves output to context.txt by default)
repo2prompt https://github.com/anthropics/skills

# Output to a specific file
repo2prompt ./my-project -o claude-context.txt
```

### What does the output look like?

The generated `context.txt` starts with a tree representation mapping out your project context:

```
# Directory Structure

📁 my-project/ (root)
  📄 main.py
  📄 package.json
  📁 src/
    📄 index.js
    📄 utils.ts
```

Followed immediately by safely-encoded UTF-8 file contents marked up nicely for standard LLM ingestion!

## 📜 Example Integrations

Simply drag the output file into:
- Claude (Opus/Sonnet)
- ChatGPT (GPT-4o)
- Google AI Studio (Gemini 1.5 Pro)

*Built by Viral as part of the weekly AI tooling initiative.*
