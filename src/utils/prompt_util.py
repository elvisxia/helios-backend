import yaml
from jinja2 import Template

BASE_PATH="../../prompts/"
class PromptUtil:
    @classmethod
    def get_prompt_from_yaml(cls,yaml_file: str,title:str):
        file_path=BASE_PATH+yaml_file
        with open(file_path,"r",encoding="utf-8") as f:
            prompts=yaml.safe_load(f)
        prompt=prompts[title]
        return prompt

    @classmethod
    def render_prompt(cls,template_str: str, **kwargs) -> str:
        template = Template(template_str)
        return template.render(**kwargs)



if __name__=="__main__":
    prompt_template=PromptUtil.get_prompt_from_yaml("memory_prompts.yaml","memory_extraction")
    text=prompt_template.format(input="哈哈，你好")
    print(text)
