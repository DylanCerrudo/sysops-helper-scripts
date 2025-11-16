#!/bin/bash

# SysOps Cron Job Setup Script
# Automates daily backups and system monitoring

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up automated cron jobs for SysOps Helper..."
echo "Project directory: $PROJECT_DIR"

# Backups the current crontab
crontab -l > /tmp/crontab_backup 2> /dev/null || true

# Created new cron jobs
# Run backup daily at 2 AM
BACKUP_JOB="0 2 * * * cd $PROJECT_DIR && /usr/bin/python3 backup_manager.py >> $PROJECT_DIR/logs/backup.log 2>&1"

# Run system_monitor every hour
MONITOR_JOB="0 * * * * cd $PROJECT_DIR && /usr/bin/python3 system_monitor.py >> $PROJECT_DIR/logs/monitor.log 2>&1"

# Check if jobs already exist
if crontab -l 2> /dev/null | grep -q "backup_manager.py"; then
	echo " Backup cron job already exists"

else
	(
		crontab -l 2> /dev/null
		echo "$BACKUP_JOB"
	)     | crontab -
	echo " Added daily backup job (runs at 2 AM)"

fi

if crontab -l 2> /dev/null | grep -q "system_monitor.py"; then
	echo "Monitor cron job already exists"

else
	(
		crontab -l 2> /dev/null
		echo "$MONITOR_JOB"
	)      | crontab -
	echo " Added hourly monitoring job"

fi

# Creates logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

echo ""
echo "Cron jobs installed successfully!"
echo ""
echo "Current cron schedule:"
crontab -l
echo ""
echo "Logs will be saved to: $PROJECT_DIR/logs/"
echo ""
echo "To view/edit cron jobs manually: crontab -e"
echo "To remove all cron jobs: crontab -r"
