from utils.utils import *



generator = NovelaiImageGenerator(mode="2", prompt_folder=env_vars["prompt_folder"], characters_path=env_vars["characters_path"])

# 加载角色列表
generator.load_characters()

generate(generator)