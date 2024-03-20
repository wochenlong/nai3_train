from utils.utils import *



# 创建 NovelaiImageGenerator 实例
generator = NovelaiImageGenerator(mode="1", prompt_folder=env_vars["prompt_folder"], characters_path=env_vars["characters_path"])

generate(generator)