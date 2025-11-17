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
    