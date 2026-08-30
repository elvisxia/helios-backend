import os

from sentence_transformers import SentenceTransformer

from utils.environment_util import load_env



# class EmbeddingUtil:
#     _model_loaded=False
#     def __init__(self):
#         load_env()
#         model_path=os.getenv("EMBEDDING_MODEL_PATH")
#         if not self._model_loaded:
#             self.model = SentenceTransformer(model_path)
#             self._model_loaded=True
#
#     def text_to_embedding(self,text:str):
#         return self.model.encode(text)
#
#     def texts_to_embeddings(self,texts:list):
#         return self.model.encode(texts)


class EmbeddingUtil:
    _model: SentenceTransformer | None = None

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            load_env()
            model_path = os.getenv("EMBEDDING_MODEL_PATH")
            cls._model = SentenceTransformer(model_path)
        return cls._model

    @classmethod
    def text_to_embedding(cls, text: str) -> list[float]:
        embedding = cls._get_model().encode(text)
        return embedding.tolist()

    @classmethod
    def texts_to_embeddings(cls, texts: list[str]) -> list[list[float]]:
        embeddings = cls._get_model().encode(texts)
        return embeddings.tolist()


if __name__=="__main__":
    embedding_util=EmbeddingUtil()
    text="这是测试text"
    embedding=embedding_util.model.encode(text)
    print(embedding)