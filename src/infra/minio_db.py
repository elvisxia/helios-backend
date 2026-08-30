import os
from datetime import timedelta

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

    def get_presigned(self,file_name:str,user_id:str):
        object_name=f"{user_id}/{file_name}"
        url=self.minio_client.presigned_get_object(bucket_name=self.bucket_name,object_name=object_name,expires=timedelta(minutes=60))
        return url


if __name__ == "__main__":
    load_env()
    db=MinIODB()
    #exists=db.minio_client.bucket_exists("helios")
    user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    file_name="test.pdf"
    url=db.get_presigned(file_name="test.pdf",user_id=user_id)
    print(url)

