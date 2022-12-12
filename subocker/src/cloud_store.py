import os
import zipfile
from google.cloud import storage

PROJECT_ID = "rectle-platform"

class CloudStore:
    def __init__(self, key_path, bucket_name):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
        self.client = storage.Client(PROJECT_ID)
        self.bucket = self.client.get_bucket(bucket_name)

    def upload(self, project_id, src_path):
        blob = self.bucket.blob("projectFiles/" + project_id + ".zip")
        blob.upload_from_filename(src_path)

    def download_and_unzip(self, src_path, dst_path, dst_file_name):
        blob = self.bucket.blob(src_path)
        blob.download_to_filename(dst_path + dst_file_name)
        with zipfile.ZipFile(dst_path + dst_file_name, 'r') as zip_ref:
            zip_ref.extractall(dst_path)