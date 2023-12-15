import random
import requests
import zipfile
import io
import os
import string
import time


class NovelaiImageGenerator:
    def __init__(self, prompt_folder, negative_prompt):
        # 初始化函数，接受两个参数：prompt_folder 和 negative_prompt
        self.token = ""  # 设置 API 的访问令牌
        self.api = "https://api.novelai.net/ai/generate-image"  # API 的地址
        self.headers = {
            "authorization": f"Bearer {self.token}",  # 设置请求头中的授权信息
            "referer": "https://novelai.net",  # 设置请求头中的 referer
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",  # 设置请求头中的 user-agent
        }
        self.json = {
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
                "negative_prompt": negative_prompt,  # 设置负面提示参数
            },
        }

        self.prompt_folder = prompt_folder

    def generate_image(self):
        # 生成图像的方法
        seed = random.randint(0, 9999999999)  # 生成一个随机种子
        self.json["parameters"]["seed"] = seed  # 将随机种子设置到请求参数中

        # 从指定文件夹中随机选择一个文本文件
        prompt_file = random.choice(os.listdir(self.prompt_folder))
        prompt_file_path = os.path.join(self.prompt_folder, prompt_file)

        # 读取文本文件内容作为 prompt 参数的值
        with open(prompt_file_path, "r") as file:
            prompt = file.read()

        self.json["input"] = (
            " masterpiece, very aesthetic "
            + prompt
        )  # 添加默认前缀
        r = requests.post(self.api, json=self.json, headers=self.headers)  # 发送 POST 请求
        with zipfile.ZipFile(
            io.BytesIO(r.content), mode="r"
        ) as zip:  # 将响应内容解压缩为 Zip 文件
            with zip.open("image_0.png") as image:  # 打开解压后的 Zip 文件中的图像文件
                return image.read()  # 返回图像的二进制数据


def save_image_from_binary(image_data, folder_path):
    # 生成随机的文件名
    file_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    file_path = os.path.join(folder_path, file_name + ".png")

    try:
        with open(file_path, "wb") as file:
            file.write(image_data)
        print("图像已保存到：", file_path)
    except IOError as e:
        print("保存图像时出错：", e)


# 创建 NovelaiImageGenerator 实例
generator = NovelaiImageGenerator(
    prompt_folder="./prompt",
    negative_prompt="nsfw",
)

# 生成图像数据
image_data = generator.generate_image()

# 图像文件的保存路径
folder_path = "./output"

# 保存图像文件
save_image_from_binary(image_data, folder_path)

# 生成多张图像并保存
num_images = 50  # 要生成的图像数量
batch_size = 10  # 每批次生成的图像数量
sleep_time = 10  # 每批次生成后的休眠时间（单位：秒）

for i in range(num_images):
    # 生成图像数据
    image_data = generator.generate_image()

    # 保存图像文件
    save_image_from_binary(image_data, folder_path)

    if (i + 1) % batch_size == 0:
        print(f"已生成 {i + 1} 张图像，休眠 {sleep_time} 秒...")
        time.sleep(sleep_time)

print("所有图像已生成完毕！")
