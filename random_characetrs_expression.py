# FIXME: 重构

import io
import os
import random
import string
import time
import zipfile

import requests
from requests.exceptions import SSLError, RequestException

import json

# 哭了 TAT
# 用户自定义 角色 JSON 文件的路径
characters_path = r".\json\genshin_poimiku.json"
# 用户自定义 表情 JSON 文件的路径
expressions_path = r".\json\expressions.json"
# 生成图像文件的保存路径
folder_path = ".\output"
# 选择读取方式(仅限角色，表情为随机读取)
read_mode = 1  # -1为随机读取，1为按顺序读取

# 设置角色优先级
role_priority = 1  # 默认为0时不生效,选择1时，把角色词优先放prefix 前面

# 选择 seed
seed = -1  # 默认随机 seed，默认随机 seed，不填或者设置为-1时为随机seed

token = None  # 目录创建一个token.txt文件夹，将你的token粘贴进去
with open("./token.txt", "r") as file:
    token = file.read()

# 生成多张图像并保存
num_images = 100  # 要生成的图像数量
batch_size = 10  # 每批次生成的图像数量
retry_delay = 20  # 每批次生成后的休眠时间（单位：秒）

sleep_time_batch_min = 1  # 每批次生成后的休眠时间最小值（单位：秒）
sleep_time_batch_max = 3  # 每批次生成后的休眠时间最小值（单位：秒）
sleep_time_single_min = 0.5  # 每张图生成后的休眠时间最小值（单位：秒）
sleep_time_single_max = 3  # 每张图生成后的休眠时间最小值（单位：秒）

retry_delay = 1  # 因为报错中断，脚本的重新启动时间（单位：秒）
prefix = "naga_u,[tyakomes],henreader,baku-p,year_2023,official art,1girl,portrait,lineart,monochrome,solo,portrait,white background, simple background, upper body,{{cropped shoulders}}, looking at viewer, hair highlight, light eyes,"  # 加在提示词前面的固定画风词或质量词
negative_prompt = "nsfw,ugly,coat,lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], lowres, {bad}, error, fewer, extra,missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan,"  # 负面提示词


class NovelaiImageGenerator:
    def __init__(self, characters_path, negative_prompt, expressions_path):
        self.token = token
        self.api = "https://api.novelai.net/ai/generate-image"
        self.headers = {
            "authorization": f"Bearer {self.token}",
            "referer": "https://novelai.net",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        self.json = {
            "input": "",
            "model": "nai-diffusion-3",
            "action": "generate",
            "parameters": {
                "width": 1024,
                "height": 1024,
                "scale": 5,
                "sampler": "k_euler",
                "steps": 28,
                "seed": 0,
                "n_samples": 1,
                "ucPreset": 0,
                "qualityToggle": "true",
                "sm": "false",
                "sm_dyn": "false",
                "dynamic_thresholding": "false",
                "controlnet_strength": 1,
                "legacy": "false",
                "add_original_image": "false",
                "uncond_scale": 1,
                "cfg_rescale": 0,
                "noise_schedule": "native",
                "negative_prompt": negative_prompt,
            },
        }

        self.characters_path = characters_path
        self.characters = []
        self.current_character_index = 0

        self.expressions_path = expressions_path
        self.expressions = []

    def load_characters(self):  # 加载角色文件
        with open(self.characters_path, "r") as file:
            data = json.load(file)
            self.characters = data["role"]

    def get_random_character(self):  # 获取随机角色文本
        return random.choice(self.characters)

    def get_next_character(self):  # 获取下一角色文本
        character = self.characters[self.current_character_index]
        self.current_character_index = (self.current_character_index + 1) % len(
            self.characters
        )
        return character

    def load_expressions(self):  # 加载表情文件
        with open(self.expressions_path, "r") as file:
            data = json.load(file)
            self.expressions = data["expression"]

    def get_random_expression(self):  # 获取随机表情文本
        return random.choice(self.expressions)

    def generate_image(self, prefix, random_mode=True, seed=None):
        if seed is None or seed == -1:
            seed = random.randint(0, 9999999999)
        self.json["parameters"]["seed"] = seed

        random_expression = self.get_random_expression()

        if random_mode:
            random_character = self.get_random_character()
        else:
            random_character = self.get_next_character()

        if role_priority == 1:
            random_character = self.get_random_character()
            self.json["input"] = random_character + prefix + random_expression
        else:
            self.json["input"] = prefix + random_character + random_expression

        r = requests.post(
            self.api, json=self.json, headers=self.headers
        )  # 将这行移动到这里，确保任何情况下都会执行
        with zipfile.ZipFile(io.BytesIO(r.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()


def save_image_from_binary(image_data, folder_path):
    file_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_path = os.path.join(folder_path, file_name + ".png")

    try:
        with open(file_path, "wb") as file:
            file.write(image_data)
        print("图像已保存到：", file_path)
    except IOError as e:
        print("保存图像时出错：", e)


generator = NovelaiImageGenerator(
    characters_path=characters_path, negative_prompt=negative_prompt, expressions_path=expressions_path
)

# 加载角色列表
generator.load_characters()
# 加载表情列表
generator.load_expressions()

# 判断读取方式
if read_mode == -1:
    random_mode = True
else:
    random_mode = False

# 生成并保存图像
image_data = generator.generate_image("prefix_", random_mode=random_mode)
save_image_from_binary(image_data, "image_folder")

for i in range(num_images):
    try:
        # 生成图像数据
        image_data = generator.generate_image(prefix)
        if image_data is None:
            continue

        # 保存图像文件
        save_image_from_binary(image_data, folder_path)

        if (i + 1) % batch_size == 0:  # 批次执行结束休眠
            sleep_time = (
                    random.uniform(sleep_time_batch_min * 100, sleep_time_batch_max * 100)
                    / 100.0
            )
            print(f"已生成 {i + 1} 张图像，休眠 {sleep_time} 秒...")
            time.sleep(sleep_time)
        else:  # 单次执行完后休眠
            sleep_time = (
                    random.uniform(sleep_time_single_min * 100, sleep_time_single_max * 100)
                    / 100.0
            )
            print(f"图像生成完毕，休眠 {sleep_time} 秒...")
            time.sleep(sleep_time)
    except (SSLError, RequestException) as e:
        print("发生错误:", e)
        print(f"休眠 {retry_delay} 秒后重新启动")
    except zipfile.BadZipFile as e:
        print("发生错误:", e)
        print("忽略此错误，继续脚本运行")
