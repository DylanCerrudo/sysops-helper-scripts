"""
Google Cloud storage backup Integration
Uploads backups to Google Cloud Storage for remote storage and disaster recovery.
"""

import os
from datetime import datetime
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError


class CloudBackupManager:
    """
    Manages backup uploads to Google Cloud Storage.
    """

    def __init__(self, bucket_name, credentials_path=None):
        """
        Initialize cloud backup manager.
        """

        self.bucket_name = bucket_name

        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(bucket_name)
            print(f"Connected to Google Cloud Storage bucket: {bucket_name}")
        except Exception as e:
            print(f"Error connecting to Google Cloud: {str(e)}")
            self.client = None
            self.bucket = None

    def upload_backup(self, local_file_path, cloud_folder="backups"):
        """
        Uploads a backup file to Google Cloud Storage.
        """

        if not self.bucket:
            print("Error: Not connected to Google Cloud Storage")
            return False

        if not os.path.exists(local_file_path):
            print("Error!: File does not exist.")
            return False

        try:
            file_name = os.path.basename(local_file_path)

            cloud_path = f"{cloud_folder}/{file_name}"

            blob = self.bucket.blob(cloud_path)

            file_size = os.path.getsize(local_file_path)
            size_mb = file_size / (1024 * 1024)

            print(f"Uploading {file_name} ({size_mb:.2f} MB) to cloud...")

            blob.upload_from_filename(local_file_path)

            print(f"Upload successful!")
            print(f"Cloud location: gs://{self.bucket_name}/{cloud_path}")

            return True

        except GoogleCloudError as e:
            print(f"Google Cloud error: {str(e)}")
            return False
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return False

    def list_cloud_backups(self, folder="backups"):
        """
        Lists all backups stored in the cloud bucket.
        """

        if not self.bucket:
            print("Error: Not Connected to Google Cloud Storage")
            return

        try:
            print(f"\n{'='*70}")
            print(f"CLOUD BACKUPS IN gs://{self.bucket_name}/{folder}/")
            print(f"{'='*70}\n")

            blobs = list(self.bucket.list_blobs(prefix=f"{folder}/"))

            if not blobs:
                print(f"No backups found in {folder}/")
                return

            blobs.sort(key=lambda x: x.time_created, reverse=True)

            for blob in blobs:

                if blob.name.endswith("/"):
                    continue

                size_mb = blob.size / (1024 * 1024)
                created = blob.time_created.strftime("%Y-%m-%d %I:%M:%S %p")

                print(f"File: {blob.name}")
                print(f"  Size: {size_mb:.2f} MB")
                print(f"  Created: {created}")
                print(f"  URL: gs://{self.bucket_name}/{blob.name}")
                print()

            print(f"Total backups: {len(blobs)}")
            print(f"{'='*70}\n")

        except Exception as e:
            print(f"Error listing cloud backups: {str(e)}")

    def download_backup(self, cloud_file_path, local_destination):
        """
        Downloads a backup from cloud storage.
        """
        if not self.bucket:
            print("Error: Not connected to Google Cloud Storage")
            return False

        try:
            blob = self.bucket.blob(cloud_file_path)

            if not blob.exists():
                print(f"Error: File not found in cloud: {cloud_file_path}")
                return False
            print(f"Downloading {cloud_file_path} from cloud...")

            blob.download_to_filename(local_destination)

            size_mb = os.path.getsize(local_destination) / (1024 * 1024)
            print(f"Download successful! ({size_mb:.2f} MB)")
            print(f"Saved to: {local_destination}")

            return True

        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return False

    def delete_old_backups(self, folder="backups", keep_count=5):
        """
        Deletes old backups from cloud, keeping only the most recent ones.
        """

        if not self.bucket:
            print("Error: Not connected to Google Cloud Storage")
            return

        try:
            blobs = list(self.bucket.list_blobs(prefix=f"{folder}/"))

            backups = [b for b in blobs if not b.name.endswith("/")]

            if len(backups) <= keep_count:
                print(f"Only {len(backups)} backups found. Nothing to delete.")
                return

            backups.sort(key=lambda x: x.time_created)

            to_delete = backups[: len(backups) - keep_count]

            print(f"Deleting {len(to_delete)} old backup(s)...")

            for blob in to_delete:
                blob.delete()
                print(f"   Deleted: {blob.name}")

            print(f"Cleanup complete! Kept {keep_count} most recent backups.")

        except Exception as e:
            print(f"Error cleaning up old backups: {str(e)}")


if __name__ == "__main__":
    print("=" * 70)
    print("GOOGLE CLOUD STORAGE BACKUP SETUP")
    print("=" * 70)
    print("\nTo use this script, you need to:")
    print("1. Create a Google Cloud account (free tier available)")
    print("2. Create a Storage bucket in Google Cloud Console")
    print("3. Create a service account and download the JSON key")
    print("4. Set the path to your credentials JSON file")
    print("\nSetup Instructions:")
    print("  https://cloud.google.com/storage/docs/creating-buckets")
    print("  https://cloud.google.com/iam/docs/service-accounts-create")
    print("\n" + "=" * 70)
    print("\nExample Usage:")
    print("=" * 70)
    print(
        """
# Initialize cloud backup manager
cloud = CloudBackupManager(
    bucket_name='your-bucket-name',
    credentials_path='path/to/credentials.json'
)

# Upload a backup
cloud.upload_backup('backups/myfile_backup_20251116.zip')

# List all cloud backups
cloud.list_cloud_backups()

# Download a backup
cloud.download_backup('backups/myfile_backup_20251116.zip', 'restored/myfile.zip')

# Clean up old backups (keep only 5 most recent)
cloud.delete_old_backups(keep_count=5)
    """
    )
    print("=" * 70)
