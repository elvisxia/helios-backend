import os

from sentence_transformers import SentenceTransformer

from utils.environment_util import load_env



class EmbeddingUtil:
    _model_loaded=False
    def __init__(self):
        load_env()
        model_path=os.getenv("EMBEDDING_MODEL_PATH")
        if not self._model_loaded:
            self.model = SentenceTransformer(model_path)
            self._model_loaded=True

    def text_to_embedding(self,text:str):
        return self.model.encode(text)

    def texts_to_embeddings(self,texts:list):
        return self.model.encode(texts)


if __name__=="__main__":
    embedding_util=EmbeddingUtil()
    text="这是测试text"
    embedding=embedding_util.model.encode(text)
    print(embedding)