"""
Automated Backup Manager
Handles files and directory backups with compression and timestamp tracking.
Improves data recovery speed through automated, organized backup creation.
"""

import os
import shutil
import zipfile
from datetime import datetime


def should_skip_file(file_path):
    """
    Determines if a file should be excluded from backup.

    """
    skip_patterns = [
        ".git",
        "__pycache__",
        ".vscode",
        "backups",
        ".DS_Store",
        "._",
    ]

    for pattern in skip_patterns:
        if pattern in file_path:
            return True

    return False


def create_backup(source_path, backup_dir="backups"):
    """
    Creates a timestamped backup of a fil or directory.

    Compresses the source into a ZIP archive with timestamp
    for easy version tracking and reduced storage usage.
    """
    # Validate that source exists before attempting backup
    if not os.path.exists(source_path):
        print(f" ✗ Error: Source path '{source_path}' does not exist")
        return None

    # Create backup directory if it doesn't exist
    # exist_ok=True prevents errors if directory already exists
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%I%M%S_%p")

    source_name = os.path.basename(source_path.rstrip("/\\"))

    backup_filename = f"{source_name}_backup_{timestamp}.zip"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        print(f"Creating backup of '{source_path}'...")

        with zipfile.ZipFile(
            backup_path, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zipf:

            if os.path.isdir(source_path):

                for root, dirs, files in os.walk(source_path):
                    for file in files:

                        file_path = os.path.join(root, file)

                        arcname = os.path.relpath(file_path, source_path)

                        if should_skip_file(file_path):
                            continue

                        zipf.write(file_path, arcname)
                        print(f" Added: {arcname}")

            else:
                zipf.write(source_path, os.path.basename(source_path))
                print(f" Added {os.path.basename(source_path)}")

        backup_size = os.path.getsize(backup_path)
        size_mb = backup_size / (1024 * 1024)  # Converts Bytes to MB

        print(f"Backup Created successfully!")
        print(f"Location: {backup_path}")
        print(f"Size: {size_mb:.2f} MB")

        return backup_path

    except PermissionError:
        print(f" ✗ Error: Permission denied accessing '{source_path}'")
        return None

    except Exception as e:
        print(f" ✗ Error creating backup: {str(e)}")
        return None


def list_backups(backup_dir="backups"):
    """
    Lists all available backups with their details.
    """

    if not os.path.exists(backup_dir):
        print(f"No backups found. Backup directory doesn't exist yet.")
        return

    backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]

    if not backup_files:
        print(f"No backups found in '{backup_dir}")
        return

    backup_files.sort(
        key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True
    )

    print(f"\n{'='*70}")
    print(f"AVAILABLE BACKUPS ({len(backup_files)} total)")
    print(f"{'='*70}\n")

    for backup in backup_files:
        backup_path = os.path.join(backup_dir, backup)

        # Get file size in MB
        size_mb = os.path.getsize(backup_path) / (1024 * 1024)

        # Get creation time
        created = datetime.fromtimestamp(os.path.getmtime(backup_path))
        created_str = created.strftime("%Y-%m-%d %I:%M:%S %p")

        print(f"   {backup}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Created: {created_str}")
        print()


def restore_backup(backup_path, restore_dir="restored"):
    """
    Restores files from a backup archive.

    """

    if not os.path.exists(backup_path):
        print(f" ✗ Error: Backup file '{backup_path}' not found")
        return False

    os.makedirs(restore_dir, exist_ok=True)

    try:
        print(f"Restoring backup from '{backup_path}'...")

        with zipfile.ZipFile(backup_path, mode="r") as zipf:
            zipf.extractall(restore_dir)

            file_list = zipf.namelist()
            print(f" ✓ Restored {len(file_list)} files to '{restore_dir}'")

            for file in file_list[:5]:
                print(f" ✓ {file}")

            if len(file_list) > 5:
                print(f" ... and {len(file_list) - 5} more files")

        return True

    except Exception as e:
        print(f" ✗ Error restoring backup: {str(e)} ")
        return False


def scheduled_backup(source_paths, backup_dir="backups"):
    """
    Performs scheduled backups for multiple sources (for cron jobs).
    Logs results instead of printing to console.
    """
    import logging

    logging.basicConfig(
        filename="logs/backup.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Starting scheduled backup")

    for source in source_paths:
        try:
            result = create_backup(source, backup_dir)
            if result:
                logging.info(f"Successfully backed up: {source}")
            else:
                logging.error(f"Failed to backup: {source}")

        except Exception as e:
            logging.error(f"Error backing up {source}: {str(e)}")

    logging.info("Scheduled backup completed!")


if __name__ == "__main__":
    print("=== AUTOMATED BACKUP MANAGER ===\n")

    print("Example 1: Creating backup of project files...")
    create_backup(".")

    print("\n" + "-" * 70 + "\n")

    print("Example 2: Listing all backups...")
    list_backups()


# Uncomment to test restore:
# print("\n" + "-"*70 + "\n")
# print("Example 3: Restoring a backup...")
# restore_backup('backups/your_backup_file.zip')
