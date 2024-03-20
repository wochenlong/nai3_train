from utils.utils import *



generator = NovelaiImageGenerator(mode="2", prompt_folder=env_vars["prompt_folder"], characters_path=env_vars["characters_path"])

# 加载角色列表
generator.load_characters()

# 生成并保存图像
image_data = generator.generate_image(env_vars["prefix"])

save_image_from_binary(image_data, env_vars["folder_path"])

generate(generator)