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
            os.environ['GOOGLE_APPLICATION_CREDENTALS'] = credentials_path
        
        
        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(bucket_name)
            print(f"Connected to Google Cloud Storage bucket: {bucket_name}")
        except Exception as e:
            print(f"Error connecting to Google Cloud: {str(e)}")
            self.client = None
            self.bucket = None

    def upload_backup(self, local_file_path, cloud_folder='backups'):
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
            size_mb = file_size /(1024 * 1024)
            
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
    
    def list_cloud_backups(self, folder='backups'):
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
                
                if blob.name.endswith('/'):
                    continue
                
                size_mb = blob.size / (1024 * 1024)
                created = blob.time_created.strftime('%Y-%m-%d %I:%M:%S %p')
                
                
                print(f"File: {blob.name}")
                print(f"  Size: {size_mb:.2f} MB")
                print(f"  Created: {created}")
                print(f"  URL: gs://{self.bucket_name}/{blob.name}")
                print()
            
            print(f"Total backups: {len(blobs)}")
            print(f"{'='*70}\n")
        
        except Exception as e:
            print(f"Error listing cloud backups: str{e}")
    
    
            
            
    