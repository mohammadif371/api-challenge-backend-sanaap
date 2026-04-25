from minio import Minio
from minio.error import S3Error
from django.conf import settings
import uuid
from datetime import timedelta


class MinioService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise Exception(f"MinIO bucket error: {e}")

    def upload_file(self, file, file_name: str) -> str:
        """
        Upload file to MinIO
        Returns: unique path of stored file
        """
        # Generate unique path to avoid name conflicts
        unique_name = f"{uuid.uuid4()}_{file_name}"
        path = f"documents/{unique_name}"

        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=path,
                data=file,
                length=file.size,
                content_type=file.content_type
            )
            return path
        except S3Error as e:
            raise Exception(f"MinIO upload error: {e}")

    def get_presigned_url(self, path: str) -> str:
        """
        Generate a secure temporary URL for file access
        URL expires after 1 hour
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=path,
                expires=timedelta(hours=1)
            )
            return url
        except S3Error as e:
            raise Exception(f"MinIO URL error: {e}")

    def delete_file(self, path: str) -> bool:
        """Delete file from MinIO"""
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=path
            )
            return True
        except S3Error as e:
            raise Exception(f"MinIO delete error: {e}")

    def update_file(self, old_path: str, new_file, new_file_name: str) -> str:
        """Delete old file and upload new one"""
        self.delete_file(old_path)
        return self.upload_file(new_file, new_file_name)