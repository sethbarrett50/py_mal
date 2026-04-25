# py-mal

`py-mal` is a Python-based malware research and educational framework containing isolated implementations of common malware techniques for **defensive research, reverse engineering practice, detection engineering, and academic study**.

This repository is intended for:

- Malware analysis education
- Reverse engineering practice
- Defensive tooling research
- Detection rule development
- Academic experimentation
- Security training environments
- Controlled sandbox testing

This project is **not intended for unauthorized deployment, malicious activity, or use against systems you do not own or explicitly have permission to test.**

---

## Disclaimer

This repository contains code that demonstrates behaviors commonly associated with malware.

Examples include:

- Reverse shells
- Remote administration tools (RATs)
- Data scraping utilities
- Command execution mechanisms
- Future implementations of:
  - Domain Generation Algorithms (DGA)
  - Command and Control (C2)
  - Privilege escalation techniques

All code should only be executed in:

- Virtual machines
- Isolated lab environments
- Sandboxes
- Academic research settings
- Authorized red team environments

You are solely responsible for how this code is used.

---

## Project Structure

```bash
src/
├── rev_shell/      # Reverse shell implementation
├── rat/            # Remote administration tooling
├── data_scrape/    # Browser/data extraction examples
├── c2/             # Future command and control implementations
├── dga/            # Future domain generation algorithms
├── priv_escal/     # Future privilege escalation examples
├── common/         # Shared utilities
```

---

## Current Modules

### Reverse Shell (`src/rev_shell`)
Demonstrates:

- Remote command execution
- Client/server communication
- Configuration handling
- Logging
- Connection lifecycle management

Example:

```bash
uv run python -m rev_shell.cli --help
```

---

### RAT (`src/rat`)
Demonstrates:

- Screen capture
- Remote command execution
- Streaming mechanisms
- Client/server communication models

Example:

```bash
uv run python -m rat.cli --help
```

---

### Data Scraping (`src/data_scrape`)
Demonstrates:

- Browser artifact discovery
- Local data extraction
- Research-focused scraping workflows

Example:

```bash
uv run python -m data_scrape.cli --help
```

---

## Installation

This project uses :contentReference[oaicite:1]{index=1} for dependency management.

### Clone repository

```bash
git clone https://github.com/yourusername/py-mal.git
cd py-mal
```

### Install dependencies

```bash
uv sync
```

---

## Running Tests

This project uses :contentReference[oaicite:2]{index=2}.

Run all tests:

```bash
uv run pytest
```

Run specific test categories:

```bash
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m smoke
```

---

## Build Package

```bash
rm -rf dist/
uv build
uv tool run twine check dist/*
```

---

## Development Standards

This repository follows:

- Modern Python packaging
- `src/` layout
- Type hints
- Modular architecture
- Unit/integration/smoke testing
- Security research reproducibility

Formatting/linting:

```bash
uv run ruff check .
uv run ruff format .
```

---

## Roadmap

Planned additions:

- Domain Generation Algorithms
- C2 simulation
- Persistence mechanisms
- Sandbox evasion examples
- Detection engineering examples
- YARA/Sigma rule generation
- Malware traffic analysis datasets

---

## License

This repository is intended for research and educational purposes.