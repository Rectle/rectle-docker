import firebase_admin
import zipfile
from firebase_admin import credentials, storage


class FireStore:
    def __init__(self, key_path, bucket_name):
        self.cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(self.cred, {'storageBucket': bucket_name})
        self.bucket = storage.bucket()

    def upload(self, project_id, src_path):
        blob = self.bucket.blob("projectFiles/" + project_id + ".zip")
        blob.upload_from_filename(src_path)

    def download_and_unzip(self, src_path, dst_path, dst_file_name):
        blob = self.bucket.blob(src_path)
        blob.download_to_filename(dst_path + dst_file_name)
        with zipfile.ZipFile(dst_path + dst_file_name, 'r') as zip_ref:
            zip_ref.extractall(dst_path)