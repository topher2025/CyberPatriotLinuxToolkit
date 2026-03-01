<!-- IGNORE -->
# CyberPatriot Linux Toolkit

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Author](https://img.shields.io/badge/Author-Christopher%20Lewis-blue.svg)](https://github.com/topher2025)


**Author:** Christopher Lewis  
**Copyright:** &copy; 2026 Christopher Lewis  
**License:** Apache License 2.0

A Linux automation and system-hardening toolkit designed to assist **CyberPatriot**
competitors during **training environments and competitions**.

This project automates common security checks while keeping all actions transparent and easily updateable.



---

## Features

- User and group auditing
- Service and daemon inspection
- File permission checks
- Common Linux hardening helpers
- Clear logging of actions taken
- Modular design for selective execution

Design goals:
- **Readable** – scripts are easy to understand and modify  
- **Modular** – run only what you need  
- **Competition-safe** – avoids destructive or rule-breaking behavior  

---

## Supported Platforms

- Linux (primarily Ubuntu-based distributions)
- Designed for CyberPatriot Linux competition images

---

## Installation

Ensure Python is installed:
```bash
python --version
```

Clone the repository:
```bash
git clone https://github.com/topher2025/CyberPatriotLinuxToolkit.git
cd CyberPatriotLinuxToolkit
```
Start virtual environment:
```bash
python3 -m venv ~/venv
source ~/venv/bin/activate
```

Run the setup file:
```bash
python3 setup.py
```

Run the script:
```bash
python3 main.py -h
```
---

## Options

| Argument              | Short | Description                                                 |
|:----------------------|:-----:|:------------------------------------------------------------|
| --readme              |  -r   | Path to competition README file                             |
| --auto-readme         |  -R   | Auto-find README in common locations                        |
| --parse-readme        |  -P   | Only parse and display README data                          |
| --dry-run             |  -d   | Preview changes without applying                            |
| --no-interactive      |  -y   | Disable interactive prompts and redirects stdout to ./logs/ |
| --password-policy     |  -p   | Password policy enforcement                                 |
| --account-permissions |  -a   | Account permissions check (requires README)                 |
| --user-management     |  -u   | User management (requires README)                           |
| --service-management  |  -s   | Service management                                          |
| --audit-policy        |  -t   | Audit policy configuration                                  |
| --firewall            |  -f   | Firewall configuration                                      |
| --security-hardening  |  -k   | Security hardening                                          |
| --media-scan          |  -m   | Prohibited media scanner                                    |
| --all                 |       | Run all tasks                                               |
| --test                |       | Run tests for supplied arguments                            |
| --help                |  -h   | Show this help message and exit                             |


## Usage Examples

## Project Structure
```
CyberPatriotLinuxToolkit/
├── README.md               # This file
├── LICENSE                 # Apache 2.0 License
├── NOTICE                  # Attribution & trademark notice
├── CREDITS.md              # Credits and insparations
├── CONTRIBUTING.md         # Contribution guidelines
├── setup.py                # Initial setup
├── main.py                 # Entry point
├── data/                   # Data and config fils
│   ├── parsed.json         # Output path for README parsing
│   ├── prohibited.json     # Prohibited items
├── modules/                # Modules for tasks
│   ├── user_mgmt/          # User & group auditing
│   ├── services/           # Service inspection
│   ├── firewall/           # Firewall checks
│   ├── hardening/          # System hardening helpers
│   └── media_scan/         # Prohibited media scanning
├── utils/                  # Shared helpers
│   ├── readme.py           # Supports README opperations
│   ├── scripts.py          # Supports shell script operations
└── tests/                  # Sample READMEs
```


## Contributing
Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch
3. **Test** your feature
4. **Commit** your changes
5. **Push** your changes to your fork
6. **Open a Pull Request** for review

Open the [CONTRIBUTIONS.md](CONTRIBUTIONS.md) for more information on contributing




## Credits

The concept and general automation approach were inspired by the following
Windows-based project:

- **Project Name:** CyberPatriotAutomation
- **Language / Platform:** C# (Windows automation)
- **Author:** Maxwell McCormick
- **Repository:** [NotMaxwell/CyberPatriotAutomation](https://github.com/NotMaxwell/CyberPatriotAutomation)

No source code, scripts, or assets from the above project were used.
All logic, structure, and implementation in this repository were written
independently for Linux systems.
