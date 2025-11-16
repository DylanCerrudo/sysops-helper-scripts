"""
Cron Job Examples for SysOps Automation
Demonstrates various scheduling patterns for system operations.
"""


def print_cron_examples():
    """
    Displays common cron scheduling patterns with explanations.
    """
    print("=" * 70)
    print("CRON JOB SCHEDULING EXAMPLES!")
    print("=" * 70)
    print("\nFormat: minute hour day month weekday command")
    print("\nCommon Patterns:\n")

    examples = [
        {
            "schedule": "0 2 * * *",
            "description": "Daily at 2:00 AM",
            "use_case": "Perfect for daily backups during off-hours",
        },
        {
            "schedule": "*/15 * * * *",
            "description": "Every 15 minutes",
            "use_case": "Frequent system monitoring for critical systems",
        },
        {
            "schedule": "0 */6 * * *",
            "description": "Every 6 hours",
            "use_case": "Regular system checks throughout the day",
        },
        {
            "schedule": "0 0 * * 0",
            "description": "Weekly on Sunday at midnight",
            "use_case": "Weekly full system backups",
        },
        {
            "schedule": "0 0 1 * *",
            "description": "Monthly on the 1st at midnight",
            "use_case": "Monthly archive backups",
        },
        {
            "schedule": "30 1 * * 1-5",
            "description": "Weekdays at 1:30 AM",
            "use_case": "Business day backups only",
        },
    ]

    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['schedule']}")
        print(f"    When: {example['description']}")
        print(f"    Use: {example['use_case']}")
        print()

    print("=" * 70)
    print("\nRECOMMENDED SCHEDULES FOR THIS PROJECT.")
    print("=" * 70)
    print("\n# Daily backups at 2 AM")
    print("0 2 * * * cd /path/to/sysops-helper && python3 backup_manager.py")
    print("\n# System monitoring every hour")
    print("0 * * * * cd /path/to/sysops-helper && python3 system_monitor.py")
    print("\n# Log analysis every 30 minutes")
    print("*/30 * * * * cd /path/to/sysops-helper && python3 log_analyzer.py")
    print("\n" + "=" * 70)
    print("\nUseful Commands:")
    print("  crontab -e    : Edit your cron jobs")
    print("  crontab -l    : List current cron jobs")
    print("  crontab -r    : Remove all cron jobs")
    print("=" * 70)


if __name__ == "__main__":
    print_cron_examples()
