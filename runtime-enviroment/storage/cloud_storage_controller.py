from google.cloud import storage
import os

class CloudStorage:
    def __init__(self, bucket_name : str = "subocker-projects") -> None:
        self.client = storage.Client.from_service_account_json("./subocker_credentials.json")
        self.bucket = self.client.get_bucket(bucket_name)

    def set_bucket(self, bucket_name: str) -> None:
        self.bucket = self.client.get_bucket(bucket_name)

    def upload_file(self, source: str, dest: str) -> None:
        file = self.bucket.blob(dest)
        file.upload_from_filename(source)

    def import_file(self, source: str, dest: str) -> None:
        file = self.bucket.blob(source)
        file.download_to_filename(dest)

storage = CloudStorage()
storage.import_file(os.environ.get('FILE_PATH'), "../src/code.py")

