import io
import random
import time
import os
import re
import requests
import shutil
import string
import zipfile

try:
    import ujson as json
except:
    import json

from dotenv import dotenv_values
from requests.exceptions import SSLError, RequestException



# 将示例配置文件复制一份并重命名, 本来是打算写进自述文件让用户自己操作的(
if os.path.exists(".env"):
    pass
else:
    shutil.copy(".env.example", ".env")
env_vars = dotenv_values('.env')

# 这一段是兼容配置, 如果根目录下存在 token.txt 则读取其中的 token, 并将其复制进 .env 中, 然后删除旧的 token.txt
if os.path.exists("./token.txt"):
    with open("./token.txt", 'r', encoding='utf-8') as file:
        token = file.read()
    with open(".env", 'r', encoding="utf-8") as file:
        data = file.read()
    # 不要动我的正则!!!
    data = re.sub(r"\stoken\s*=\s*\"(.*?)\"", f"\ntoken = \"{token}\"", data)
    with open(".env", 'w', encoding="utf-8") as file:
        file.write(data)
    os.remove("./token.txt")
# 改善用户体验, 让用户可以直接在命令行中粘贴获取到的 token
elif env_vars["token"] == "":
    token = input("输入获取到的 token:")
    with open(".env", 'r', encoding="utf-8") as file:
        data = file.read()
    data = re.sub(r"\stoken\s*=\s*\"(.*?)\"", f"\ntoken = \"{token}\"", data)
    with open(".env", 'w', encoding="utf-8") as file:
        file.write(data)
else:
    pass
# 由于上方的文件操作进行第二次读取
env_vars = dotenv_values('.env')
token = env_vars["token"]

if os.path.exists(env_vars["folder_path"]):
    pass
else:
    os.makedirs(env_vars["folder_path"])



headers = {
    "authorization": f"Bearer {token}",  # 设置请求头中的授权信息
    "referer": "https://novelai.net",  # 设置请求头中的 referer
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",  # 设置请求头中的 user-agent
}
json_ = {
    "input": "",  # 设置请求的输入文本
    "model": "nai-diffusion-3",  # 设置模型名称
    "action": "generate",  # 设置动作为生成图像
    "parameters": {
        "width": 832,  # 设置生成图像的宽度
        "height": 1216,  # 设置生成图像的高度
        "scale": 5,  # 设置图像的缩放比例
        "sampler": "k_euler",  # 设置采样器类型
        "steps": 28,  # 设置生成图像的步数
        "seed": 0,  # 设置生成图像的随机种子
        "n_samples": 1,  # 设置生成图像的样本数
        "ucPreset": 0,  # 设置 ucPreset 参数
        "qualityToggle": "true",  # 设置 qualityToggle 参数
        "sm": "false",  # 设置 sm 参数
        "sm_dyn": "false",  # 设置 sm_dyn 参数
        "dynamic_thresholding": "false",  # 设置 dynamic_thresholding 参数
        "controlnet_strength": 1,  # 设置 controlnet_strength 参数
        "legacy": "false",  # 设置 legacy 参数
        "add_original_image": "false",  # 设置 add_original_image 参数
        "uncond_scale": 1,  # 设置 uncond_scale 参数
        "cfg_rescale": 0,  # 设置 cfg_rescale 参数
        "noise_schedule": "native",  # 设置 noise_schedule 参数
        "negative_prompt": env_vars["negative_prompt"],  # 设置负面提示参数
    },
}


class NovelaiImageGenerator:
    def __init__(self, mode, prompt_folder, characters_path):
        self.mode = mode
        
        # 初始化函数，接受两个参数：prompt_folder 和 negative_prompt
        self.token = token
        self.api = "https://api.novelai.net/ai/generate-image"  # API 的地址
        self.headers = headers
        self.json_ = json_

        self.prompt_folder = prompt_folder

        self.characters_path = characters_path
        self.characters = []
        self.current_character_index = 0

    def load_characters(self):
        with open(self.characters_path, "r") as file:
            data = json.load(file)
            self.characters = data["role"]

    def get_random_character(self):
        return random.choice(self.characters)

    def get_next_character(self):
        character = self.characters[self.current_character_index]
        self.current_character_index = (self.current_character_index + 1) % len(
            self.characters
        )
        return character

    def generate_image(self, prefix):
        try:
            # 生成图像的方法
            seed = random.randint(0, 9999999999)  # 生成一个随机种子
            self.json_["parameters"]["seed"] = seed  # 将随机种子设置到请求参数中

            # 从指定文件夹中随机选择一个文本文件
            prompt_file = random.choice(os.listdir(self.prompt_folder))
            prompt_file_path = os.path.join(self.prompt_folder, prompt_file)

            # 读取文本文件内容作为 prompt 参数的值
            with open(prompt_file_path, "r") as file:
                prompt = file.read()

            if self.mode == "1":
                str_artist = get_random_artist()
                # self.json_["input"] = prefix + prompt  # 添加自定义前缀
                self.json_["input"] = str_artist + prefix  # 添加自定义前缀
            elif self.mode == "2":
                if env_vars["read_mode"] == -1:
                    random_character = self.get_random_character()
                else:
                    random_character = self.get_next_character()
                if env_vars["role_priority"] == 1:
                    # random_character = self.get_random_character()
                    self.json_["input"] = random_character + prefix
                else:
                    self.json_["input"] = prefix + random_character
            elif self.mode == "3":
                self.json_["input"] = prefix + prompt  # 添加自定义前缀
            else:
                print("输入有误!")
                raise ValueError

            r = requests.post(
                self.api, json=self.json_, headers=self.headers
            )  # 发送 POST 请求
            r.raise_for_status()  # 如果请求返回的状态码不是 2xx，会抛出异常

            with zipfile.ZipFile(
                io.BytesIO(r.content), mode="r"
            ) as zip:  # 将响应内容解压缩为 Zip 文件
                with zip.open(
                    "image_0.png"
                ) as image:  # 打开解压后的 Zip 文件中的图像文件
                    return image.read()  # 返回图像的二进制数据

        except requests.exceptions.RequestException as e:
            print("请求出现异常:", e)
        except Exception as e:
            print("捕获到未处理的异常:", e)


def generate(generator):
    for i in range(int(env_vars["num_images"])):
        try:
            # 生成图像数据
            image_data = generator.generate_image(env_vars["prefix"])
            if image_data is None:
                continue

            # 保存图像文件
            save_image_from_binary(image_data, env_vars["folder_path"])

            if (i + 1) % int(env_vars["batch_size"]) == 0:  # 批次执行结束休眠
                sleep_time = (
                    random.uniform(float(env_vars["sleep_time_batch_min"]) * 100, float(env_vars["sleep_time_batch_max"]) * 100)
                    / 100.0
                )
                print(f"已生成 {i + 1} 张图像，休眠 {sleep_time} 秒...")
                time.sleep(sleep_time)
            else:  # 单次执行完后休眠
                sleep_time = (
                    random.uniform(float(env_vars["sleep_time_single_min"]) * 100, float(env_vars["sleep_time_single_max"]) * 100)
                    / 100.0
                )
                print(f"图像生成完毕，休眠 {sleep_time} 秒...")
                time.sleep(sleep_time)
        except (SSLError, RequestException) as e:
            print("发生错误:", e)
            t = float(env_vars["retry_delay"])
            print(f"休眠 {t} 秒后重新启动")
        except zipfile.BadZipFile as e:
            print("发生错误:", e)
            print("忽略此错误，继续脚本运行")


def save_image_from_binary(image_data, folder_path):
    file_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_path = os.path.join(folder_path, file_name + ".png")

    try:
        with open(file_path, "wb") as file:
            file.write(image_data)
        print("图像已保存到：", file_path)
    except IOError as e:
        print("保存图像时出错：", e)


def get_random_artist():
    artist_num = random.randrange(5, 11)  # 抽取5个到10个画师
    artist_list = str(re.findall('\[(.*?)\]', env_vars["artists"])[0]).replace("\"", '').split(", ")
    random_selection = random.sample(artist_list, artist_num)
    random.shuffle(random_selection)
    _ = "artist:" + ",artist:".join(random_selection)
    print(f"抽取随机画师串 {_}")
    return _