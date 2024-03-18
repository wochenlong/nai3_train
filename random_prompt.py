import random
import requests
import zipfile
import io
import os
import zipfile


from utils.utils import *



class NovelaiImageGenerator:
    def __init__(self, prompt_folder):
        # 初始化函数，接受两个参数：prompt_folder 和 negative_prompt
        self.token = token
        self.api = "https://api.novelai.net/ai/generate-image"  # API 的地址
        self.headers = headers
        self.json = json_
        self.prompt_folder = prompt_folder

    def generate_image(self, prefix):
        try:
            # 生成图像的方法
            seed = random.randint(0, 9999999999)  # 生成一个随机种子
            self.json["parameters"]["seed"] = seed  # 将随机种子设置到请求参数中

            # 从指定文件夹中随机选择一个文本文件
            prompt_file = random.choice(os.listdir(self.prompt_folder))
            prompt_file_path = os.path.join(self.prompt_folder, prompt_file)

            # 读取文本文件内容作为 prompt 参数的值
            with open(prompt_file_path, "r") as file:
                prompt = file.read()

            self.json["input"] = prefix + prompt  # 添加自定义前缀
            r = requests.post(
                self.api, json=self.json, headers=self.headers
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



# 创建 NovelaiImageGenerator 实例
generator = NovelaiImageGenerator(prompt_folder=env_vars["prompt_folder"])

generate(generator)