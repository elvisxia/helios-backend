import ast
import mimetypes
import uuid
from datetime import datetime, timezone

from app.models.dao.file_meta import FileMeta
from app.models.service_result import ServiceResult

from utils.llm_util import LLMUtil
from utils.embedding_util import EmbeddingUtil
from utils.prompt_util import PromptUtil


class FileService:
    def __init__(self,file_meta_dao,file_dao):
        self.file_meta_dao = file_meta_dao
        self.file_dao = file_dao


    def create_upload_url(self,file_name:str,user_id:str):
        url=self.file_dao.create_upload_url(file_name=file_name,user_id=user_id)
        data={
            "url":url,
            "file_name":file_name
        }
        return ServiceResult.ok(data=data)

    def create_delete_url(self, file_name: str, user_id: str):
        url=self.file_dao.create_delete_url(file_name=file_name,user_id=user_id)
        data={
            "url":url,
            "file_name":file_name
        }
        return ServiceResult.ok(data=data)

    def create_download_url(self,file_name:str,user_id:str):
        url=self.file_dao.create_download_url(file_name=file_name,user_id=user_id)
        data={
            "url":url,
            "file_name":file_name
        }
        return ServiceResult.ok(data=data)

    def save_file_metas(self,file_list:list[str],text:str,user_id:str):
        prompt_template=PromptUtil.get_prompt_from_yaml("file_prompts.yaml","file_info_extraction")
        prompt=PromptUtil.render_prompt(prompt_template,attachment_list=file_list,user_message=text)
        res= LLMUtil.invoke(prompt=prompt)
        result=ast.literal_eval(res.content)
        # {'attachments': [{'file_name': '可爱的卡通人物形象.png', 'description': '我的头像文件'}, {'file_name': '老鼠举重.jpg', 'description': '我的头像文件'}]}
        file_metas=self.attachments_to_file_metas(attachments=result['attachments'],user_id=user_id)
        res=self.file_meta_dao.save_file_metas(file_metas=file_metas)
        if res["insert_count"] and res["insert_count"]>0:
            return f"成功保存 {res["insert_count"]} 个文件！"
        else:
            return f"保存失败！file_meta_dao.save_file_metas 输出：{res}"


    def attachments_to_file_metas(self,attachments:list[dict],user_id:str)->list[FileMeta]:
        file_metas: list[FileMeta] = []
        for attachment in attachments:
            file_name = attachment["file_name"]
            description = attachment.get("description", "")
            # text 字段用 description，如果没有则退化为 file_name
            text = description or file_name
            file_meta = FileMeta(
                id=str(uuid.uuid4()),
                embedding=EmbeddingUtil.text_to_embedding(text),
                text=text,
                user_id=user_id,
                file_path=f"{user_id}/{file_name}",
                create_time=datetime.now(timezone.utc).isoformat(),
            )
            file_metas.append(file_meta)
        return file_metas


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
    #res=file_service.query_files(text="测试文件",user_id=user_id)
    file_list=[""]
    res=file_service.save_files_metas(file_list=["可爱的卡通人物形象.png","老鼠举重.jpg"],text="这两张都是我的头像文件",user_id=user_id)

    print(res)