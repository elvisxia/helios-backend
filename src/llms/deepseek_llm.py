from langchain.chat_models import init_chat_model
import os

from utils.environment_util import load_env

load_env()

deepseek_api_key=os.getenv("DEEPSEEK_API_KEY")
deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL")

deepseek_llm=init_chat_model(
    model="deepseek-v4-pro",
    model_provider="deepseek",
    api_key=deepseek_api_key,
    base_url=deepseek_base_url,
)