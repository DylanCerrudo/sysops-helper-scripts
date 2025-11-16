# SysOps Helper Scripts

Python automation tools I built to help with system administration tasks - log analysis, backups, and monitoring.

## What This Does

I created three main scripts that automate common sysops tasks:

**Log Analyzer** - Scans through log files and pulls out errors, warnings, and critical issues. Uses regex to parse different log formats and categorize problems by severity. Saves a ton of time when troubleshooting.

**Backup Manager** - Automatically creates timestamped ZIP backups of files and directories. Filters out junk like .git folders and build artifacts. Keeps track of backup history so you can see what got backed up when.

**System Monitor** - Watches CPU, memory, and disk usage in real-time. Set your own thresholds and get alerts when resources are running low. Can run continuously or just do spot checks.

## Setup

You'll need Python 3 and the psutil library:
```bash
pip3 install psutil --break-system-packages
```

Then clone the repo:
```bash
git clone https://github.com/DylanCerrudo/sysops-helper-scripts.git
cd sysops-helper-scripts
```

## How to Use

**Check logs:**
```bash
python3 log_analyzer.py
```
Point it at a log file and it'll show you all errors, warnings, and critical issues with timestamps.

**Create a backup:**
```bash
python3 backup_manager.py
```
Makes a compressed backup with the current date/time in the filename. Run it again later and you'll have a history of backups to choose from.

**Monitor your system:**
```bash
python3 system_monitor.py
```
Shows current CPU, RAM, and disk usage. Edit the thresholds in the code if you want alerts at different levels.

## Project Structure
```
log_analyzer.py       - parses logs and detects errors
backup_manager.py     - creates and manages backups
system_monitor.py     - tracks system resources
sample_app.log        - example log file for testing
backups/              - where backups get saved
```

## Why I Built This

I'm working on the Google IT Automation with Python certification and wanted to apply what I'm learning to real problems. As I code daily and work with multiple projects, I kept running into the same tedious tasks - manually checking logs when something breaks, remembering to backup my work, and wondering if my system was about to crash because I had too many things running.

Built these scripts to solve my own workflow issues. Now instead of digging through log files for 20 minutes, the analyzer pulls errors instantly. Backups actually happen on schedule instead of "I'll do it later" (which usually meant never). And I can glance at system stats instead of guessing if I need to close some tabs.

Basically took the repetitive stuff I was doing manually and automated it. Makes my daily coding routine way smoother.

## What's Next

Planning to add:
- Cloud storage integration (probably Google Cloud)
- Email/SMS alerts when thresholds are hit
- Cron job examples for automated scheduling
- Maybe a simple web dashboard

## Notes

The email alert code is in there but commented out - you need to add your own SMTP credentials if you want to use it. Don't push credentials to GitHub (learned that the hard way).

---

Still working on this - started October 2025, aiming to wrap up by end of November.