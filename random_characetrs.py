from utils.utils import *



generator = NovelaiImageGenerator(mode="2", prompt_folder=env_vars["prompt_folder"], characters_path=env_vars["characters_path"])

generate(generator)