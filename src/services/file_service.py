import mimetypes

from sympy import false, true

from daos import file_dao


class FileService:
    def __init__(self,file_meta_dao,file_dao):
        self.file_meta_dao = file_meta_dao
        self.file_dao = file_dao

    def save_file(self,text:str,file_name:str,user_id:str):
        """
        存储文件
        Args:
            text: 文件的备注
            file_path: 文件路径
        Returns:
            存储结果
        """
        # 服务器端的文件地址是 用户id\\文件名
        base_path="../../files"
        file_path=f"{base_path}/{user_id}/{file_name}"
        mime_type,_ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        #定义状态
        save_file_res = None
        save_meta_res = None
        # 1. 先存储文件到minio
        try:
            save_file_res=self.file_dao.upload_file(
                file_name=file_name,
                folder_name=user_id,
                file_path=file_path,
                content_type=mime_type
            )
            # 2. 存储文件meta到milvus
            minio_file_path=f"{user_id}/{file_name}"
            save_meta_res=self.file_meta_dao.save_file_meta(
                    text=text,
                    file_path=minio_file_path,
                    user_id=user_id,
                )
            return "save successfully"
        except Exception as e:
            print("保存失败：",e)
            # MinIO 已经成功 → 删除 MinIO
            if save_file_res is not None:
                try:
                    self.file_dao.delete_file(
                        file_path=file_path
                    )
                except Exception as rollback_error:
                    print(f"MinIO 回滚失败: {rollback_error}")
            if save_meta_res is not None:
                try:
                    ids = list(save_meta_res["ids"])

                    self.file_meta_dao.delete_file(
                        ids=ids
                    )
                except Exception as rollback_error:
                    print(f"Milvus 回滚失败: {rollback_error}")

    def delete_file(self,text:str,user_id:str):
        """
        删除文件和它的meta data
        Args:
            text: 文件的查询文本
            user_id: 用户id

        Returns:
            删除结果
        """
        # 1. 查询file_meta
        file_metas=self.file_meta_dao.search_file_meta(text=text,user_id=user_id)
        if len(file_metas)==0:
            return "未查询到结果"
        file_meta=file_metas[0]
        file_path=file_meta["file_path"]
        # 3. 删除文件
        try:
            self.file_dao.delete_file(file_path=file_path)
            return "deleted successfully"
        except Exception as rollback_error:
            print(rollback_error)
            return "delete failed"

    def query_files(self,text:str,user_id:str):
        """
        根据查询文本查询文件
        Args:
            text: 查询文本
            user_id: 用户id

        Returns:
            服务器上临时文件的path
        """
        # 1. 查询文件meta
        file_meta=self.get_file_meta(text=text,user_id=user_id)
        file_path=file_meta['file_path']
        # 2. 获取文件
        try:
            res=self.file_dao.get_file(file_path=file_path)
            #Object(bucket_name='helios', object_name='c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5/test.pdf', last_modified=datetime.datetime(2026, 8, 21, 6, 39, 42, tzinfo=datetime.timezone.utc), etag='290754a9b1fa76f65ddfb75826b83dfe', size=1410231, metadata=HTTPHeaderDict({'Accept-Ranges': 'bytes', 'Content-Length': '1410231', 'Content-Type': 'application/pdf', 'ETag': '"290754a9b1fa76f65ddfb75826b83dfe"', 'Last-Modified': 'Fri, 21 Aug 2026 06:39:42 GMT', 'Server': 'MinIO', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Vary': 'Origin, Accept-Encoding', 'X-Amz-Id-2': 'dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8', 'X-Amz-Request-Id': '18CDBECD63CEB0D2', 'X-Content-Type-Options': 'nosniff', 'X-Ratelimit-Limit': '2051', 'X-Ratelimit-Remaining': '2051', 'X-Xss-Protection': '1; mode=block', 'Date': 'Fri, 21 Aug 2026 06:40:16 GMT'}), version_id=None, is_latest=None, storage_class=None, owner_id=None, owner_name=None, content_type='application/pdf', is_delete_marker=False, tags=None, is_dir=False)
            return res.object_name
        except Exception as rollback_error:
            print(rollback_error)
            return "文件不存在"




    def get_file_meta(self,text:str,user_id:str):
        file_metas=self.file_meta_dao.search_file_meta(text=text,user_id=user_id)
        if len(file_metas)==0:
            return None
        else:
            return file_metas[0]






if __name__=="__main__":
    from utils.container import container
    file_service=container.file_service
    user_id="c404fa4e-8cdc-4b0b-8ea1-5ca862e042d5"
    #res=file_service.save_file(text="测试文件",file_name="test.pdf",user_id=user_id)
    #print(res)

    #res=file_service.delete_file(text="测试文件",user_id=user_id)
    res=file_service.query_files(text="测试文件",user_id=user_id)
    print(res)