from minio.helpers import ObjectWriteResult


class FileDAO:
    def __init__(self,minio_client):
        self.minio_client=minio_client

    def upload_file(self,folder_name:str,file_name:str,file_path:str,content_type:str):
        """
        上传文件到minio
        Args:
            folder_name: minio的folder ；name
            file_name: minio里的file name
            file_path: 服务器端的file path
            content_type: 文件类型
        Returns:
            返回存储结果 ex：ObjectWriteResult(bucket_name='helios', object_name='test/test.pdf', version_id=None, etag='290754a9b1fa76f65ddfb75826b83dfe', http_headers=HTTPHeaderDict({'Accept-Ranges': 'bytes', 'Content-Length': '0', 'ETag': '"290754a9b1fa76f65ddfb75826b83dfe"', 'Server': 'MinIO', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Vary': 'Origin, Accept-Encoding', 'X-Amz-Id-2': 'dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8', 'X-Amz-Request-Id': '18CD5A385D588604', 'X-Content-Type-Options': 'nosniff', 'X-Ratelimit-Limit': '2051', 'X-Ratelimit-Remaining': '2051', 'X-Xss-Protection': '1; mode=block', 'Date': 'Wed, 19 Aug 2026 23:57:05 GMT'}), last_modified=None, location=None)
        """
        res=self.minio_client.fput_object(
            bucket_name="helios",
            object_name=f"{folder_name}/{file_name}",
            file_path=file_path,
            content_type=content_type
        )
        return res

    def get_file(self,file_path:str):
        """
        获取minio中的文件
        Args:
            file_path: 文件路径

        Returns:
            获取结果 ex:Object(bucket_name='helios', object_name='test/test.pdf', last_modified=datetime.datetime(2026, 8, 19, 23, 57, 5, tzinfo=datetime.timezone.utc), etag='290754a9b1fa76f65ddfb75826b83dfe', size=1410231, metadata=HTTPHeaderDict({'Accept-Ranges': 'bytes', 'Content-Length': '1410231', 'Content-Type': 'application/pdf', 'ETag': '"290754a9b1fa76f65ddfb75826b83dfe"', 'Last-Modified': 'Wed, 19 Aug 2026 23:57:05 GMT', 'Server': 'MinIO', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Vary': 'Origin, Accept-Encoding', 'X-Amz-Id-2': 'dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8', 'X-Amz-Request-Id': '18CD5C62576B289E', 'X-Content-Type-Options': 'nosniff', 'X-Ratelimit-Limit': '2051', 'X-Ratelimit-Remaining': '2051', 'X-Xss-Protection': '1; mode=block', 'Date': 'Thu, 20 Aug 2026 00:36:44 GMT'}), version_id=None, is_latest=None, storage_class=None, owner_id=None, owner_name=None, content_type='application/pdf', is_delete_marker=False, tags=None, is_dir=False)
        """
        res=self.minio_client.fget_object(
            bucket_name="helios",
            object_name=file_path,
            file_path=f"../../files/download/{file_path}"
        )
        return res
    def delete_file(self,file_path:str):
        """
        删除minio中的文件
        Args:
            file_path: 文件路径

        Returns:
            None
        """
        self.minio_client.remove_object(
            bucket_name="helios",
            object_name=file_path
        )

if __name__=="__main__":
    from utils.container import container
    # res:ObjectWriteResult=container.file_dao.upload_file(folder_name="test",
    #                                    file_name="test.pdf",
    #                                    file_path="../../files/Attention Is All You Need.pdf",
    #                                    content_type="application/pdf")

    #res=container.file_dao.get_file(file_path="test/test.pdf")
    res=container.file_dao.delete_file("test/test.pdf")
    print(res)
