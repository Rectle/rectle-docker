from google.cloud import storage
from zipfile import ZipFile
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


if __name__ == "__main__":
    path_to_zipfile = "../project/src/files.zip"
    storage = CloudStorage()
    storage.import_file(os.environ.get('FILE_PATH'), path_to_zipfile)
    with ZipFile(path_to_zipfile, 'r') as zip_ref:
        zip_ref.extractall("../project/src/")

