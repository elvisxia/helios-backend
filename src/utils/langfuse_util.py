
from langfuse import Langfuse

from utils.environment_util import load_env


class LangfuseUtil:

    _client = None


    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = Langfuse()

        return cls._client


    @classmethod
    def get_prompt(
        cls,
        prompt_name: str,
        variables: dict = None
    ):
        """
        获取 Langfuse Prompt 并完成变量替换

        :param prompt_name: Langfuse中的prompt名称
        :param variables: prompt变量
        :param label: prompt环境标签
        """

        prompt = cls.get_client().get_prompt(
            prompt_name,
            label="production"
        )

        if variables:
            return prompt.compile(
                **variables
            )

        return prompt.compile()



if __name__=="__main__":
    load_env()
    prompt=LangfuseUtil.get_prompt("system_prompt",None)
    print(prompt)