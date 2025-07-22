import os

def load_prompt_template(filename, variables=None):
    """
    从prompts目录读取模板文件，并用variables字典填充变量。
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    prompt_path = os.path.join(base_dir, "prompts", filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    if variables:
        for k, v in variables.items():
            template = template.replace(f"{{{k}}}", str(v))
    return template 