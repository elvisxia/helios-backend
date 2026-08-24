import os

from minio import Minio

from utils.environment_util import load_env


class MinIODB:
    def __init__(self):
        access_key=os.environ.get("MINIO_ACCESS_KEY")
        secret_key=os.environ.get("MINIO_SECRET_KEY")
        end_point=os.environ.get("MINIO_END_POINT")
        self.minio_client=Minio(
            endpoint=end_point,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        self.bucket_name="helios"


if __name__ == "__main__":
    load_env()
    db=MinIODB()
    exists=db.minio_client.bucket_exists("helios")
    print(exists)

