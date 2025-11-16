"""
System Monitoring & Alerting
Real-Time system resource monitoring with threshold-based alerts.
Tracks CPU, memory, and disk usage to prevent system issues.
"""

import psutil
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SystemMonitor:
    """
    Monitors System resources and triggers alerts when thresholds are exceeded.
    """

    def __init__(self, cpu_threshold=80, memory_threshold=85, disk_threshold=90):
        """
        Initialize the system monitor with alert thresholds.
        """
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.alert_log = []

    def get_system_stats(self):
        """
        Collects current system resource usage statistics.
        """

        cpu_percent = psutil.cpu_percent(interval=1)

        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        disk = psutil.disk_usage("/")
        disk_percent = disk.percent

        cpu_count = psutil.cpu_count()
        memory_total_gb = memory.total / (1024**3)
        memory_used_gb = memory.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        disk_used_gb = disk_used_gb / (1024**3)

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d % I:%M:%S %p"),
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "memory_percent": memory_percent,
            "memory_total_gb": round(memory_total_gb, 2),
            "memory_used_gb": round(memory_used_gb, 2),
            "disk_percent": disk_percent,
            "disk_total_gb": round(disk_total_gb, 2),
            "disk_used_gb": round(disk_used_gb, 2),
        }

    def check_thresholds(self, stats):
        """
        Checks if any resource usage exceeds defined thresholds.
        """

        alerts = []

        # Check CPU threshold
        if stats["cpu_percent"] > self.cpu_threshold:
            alerts.append(
                f"HIGH CPU USAGE: {stats['cpu_percent']:.1f}% "
                f"(Threshold: {self.cpu_threshold}%)"
            )

        if stats["memory_percent"] > self.memory_threshold:
            alerts.append(
                f"HIGH MEMORY USAGE: {stats['memory_percent']:.1f}% "
                f"{stats['memory_used_gb']:.1f}GB / {stats['memory_total_gb']:.1f}GB"
                f"(Threshold: {self.memory_threshold}%)"
            )

        if stats["disk_percent"] > self.disk_threshold:
            alerts.append(
                f"HIGH DISK USAGE: {stats['disk_percent']:.1f}% "
                f"{stats['disk_used_gb']:.1f}GB / {stats['disk_total_gb']:.1f}GB"
                f"(Threshold: {self.disk_threshold}%)"
            )

        return alerts

    def display_stats(self, stats, alerts=None):
        """
        Displays system statistics in a formatted way.
        """

        print(f"\n{'='*70}")
        print(f"SYSTEM MONITORING REPORT - {stats['timestamp']}")
        print(f"{'='*70}\n")

        # CPU info
        print(f"CPU Usage:")
        print(f"    {stats['Cpu_percent']:.1f%} ({stats['cpu_count']} cores)")

        if stats["cpu_percent"] > self.cpu_threshold:
            print(f" ALERT!: Exceeds threshold ({self.cpu_threshold}%)")
        print()

        # Memory Info
        print(f" Memory Usage:")
        print(
            f" {stats['memory_percent']:.1f}% "
            f"({stats['memory_used_gb']:1f}GB / {stats['memory_total_gb']:1f}GB)"
        )
        if stats["memory_percent"] > self.memory_threshold:
            print(f"    Alert!: Exceeds threshold ({self.memory_threshold}%)")
        print()

        # Disk Info
        print(f" Disk Usage:")
        print(
            f"    {stats['disk_percent']:.1f}% "
            f"({stats['disk_used_gb']:.1f}GB / {stats['disk_total_gb']:.1f}GB)"
        )
        if stats["disk_percent"] > self.disk_threshold:
            print(f"    ALERT!: Exceeds threshold ({self.disk_threshold}%)")
        print()

    def send_email_alert(self, alerts, stats, email_config):
        """
        Sends email notification when alerts are triggered.
        """

        try:
            msg = MIMEMultipart()
            msg["From"] = email_config["sender_email"]
            msg["To"] = email_config["recipient_email"]
            msg["Subject"] = f" System Alert - {stats['timestamp']}"

            # Create email body
            body = f"""
System Monitoring Alert

Timestamp: {stats['timestamp']}

Alerts:
{chr(10).join(alerts)}

CURRENT SYSTEM STATUS:
- CPU Usage: {stats['cpu_percent']:.1f}%
- Memory Usage: {stats['memory_percent']:.1f}% ({stats['memory_used_gb']:.1f}GB / {stats['memory_total_gb']:.1f}GB)
- Disk Usage: {stats['disk_percent']:.1f}% ({stats['disk_used_gb']:.1f}GB / {stats['disk_total_gb']:.1f}GB)

This is an automated alert from your SysOps monitoring system.
            """

            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(
                email_config["smtp_server"], email_config["smtp_port"]
            )
            server.starttls()
            server.login(email_config["sender_email"], email_config["smtp_port"])
            server.send_message(msg)
            server.quit()

            print(f" Alert email sent to {email_config['recipient_email']}")
            return True

        except Exception as e:
            print(f" Failed to send email alert: {str(e)}")
            return False

    def monitor_once(self):
        """
        Performs a single monitoring check and displays results.
        """
        stats = self.get_system_stats
        alerts = self.check_thresholds
        self.display_stats(stats, alerts)
        
        if alerts:
            
            self.alert_log.append({
                'timestamp': stats['timestamp'],
                'alerts': alerts
            })
        
        return stats, alerts
    
    
        
