# Repo2Prompt

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A lightweight, zero-dependency CLI tool that cleanly packages entire local directories or remote GitHub repositories into a single LLM-optimized context prompt.

## Key Features

- **Token-Aware Chunking**: Automatically splits large repositories into multiple prompt files via `tiktoken` to respect LLM context limits.
- **Strict `.gitignore` Compliance**: Uses POSIX-normalized routing to cleanly exclude caches, node modules, and arbitrary ignored paths.
- **Smart Formatting**: Embeds a visualized directory tree to prime the LLM's spatial understanding, followed by prioritized source files (READMEs and entry points first).
- **Remote Git Support**: Provide any open repository URL; the tool securely clones, processes, and auto-cleans it locally.

## Installation

```bash
git clone https://github.com/Viralpatelz/Repo2Prompt.git
cd Repo2Prompt
pip install -e .
```

*Note: Requires Python 3.8+*

## Usage

Process either a local target or external repository:

```bash
# General syntax: repo2prompt <target> [args]
repo2prompt . 
repo2prompt https://github.com/anthropics/skills
```

### Advanced Flags

```bash
# Customize output architecture and token splitting 
repo2prompt . --output claude_bot_ctx --max-tokens 80000 --mode improve
```

## Output Architecture 

Outputs are cleanly staged. A standard output sequence resembles: 

```text
# Directory Structure

📁 my-project/ (root)
  📄 main.py
  📁 src/
    📄 utils.ts

============================================================
File: main.py
============================================================

# ... [File payload] ...
```

## CI/CD and Static Analysis
Configured with out-of-the-box `sonar-project.properties` and integrated PyTest validation suite to eliminate generic environment warnings.

---

### Changelog

**v0.1.1 (Current)**
- Integrated `tiktoken` heuristic chunking matrices.
- Added strict multi-platform file ranking prioritizations. 
- Patched Windows-centric `.gitignore` evaluation discrepancies.
- Added foundational PyTest validation suite.

**v0.1.0**
- Initial core extraction logic.
