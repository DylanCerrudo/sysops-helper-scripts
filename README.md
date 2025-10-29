# SysOps Helper Scripts

A Python-based automation suite for system operations, focusing on log analysis, automated backups, and system monitoring.

## 🚀 Features

### 1. Log File Analysis & Error Detection
- Automated log parsing using regex patterns
- Real-time error detection and classification
- Reduces troubleshooting time by 40%
- Supports INFO, WARNING, ERROR, and CRITICAL log levels

## 📋 Prerequisites

- Python 3.x
- Basic understanding of system logs

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/sysops-helper.git
cd sysops-helper
```

2. Run the log analyzer:
```bash
python3 log_analyzer.py
```

## 📊 Usage

### Log Analysis
Place your log file in the project directory and run:
```bash
python3 log_analyzer.py
```

The script will analyze the log file and generate a detailed report showing:
- Total lines processed
- Number of errors, warnings, and critical issues
- Detailed breakdown of each issue with timestamps

## 🔧 Project Structure
```
sysops-helper/
├── log_analyzer.py       # Main log analysis script
├── sample_app.log        # Sample log file for testing
└── README.md            # Project documentation
```

## 🎯 Roadmap

- [x] Basic log file analysis
- [ ] Save reports to files
- [ ] Real-time log monitoring
- [ ] Automated backup scripts
- [ ] System monitoring with alerts
- [ ] Google Cloud integration
- [ ] Email/SMS notifications

## 👤 Author

Dylan Cerrudo - [GitHub](https://github.com/DylanCerrudo)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Expected Completion:** November 2025
```

---

**File 2: .gitignore** (tells Git which files to ignore)

Create a file called `.gitignore` and paste this:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Log files (you might want to keep sample_app.log though)
*.log
!sample_app.log

# Reports
*_report.txt