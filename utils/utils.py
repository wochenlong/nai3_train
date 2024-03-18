import random
import time
import os
import re
import string
import zipfile

from dotenv import dotenv_values
from requests.exceptions import SSLError, RequestException

env_vars = dotenv_values('.env')


token = env_vars["token"] if env_vars["token"] != "" else print("请配置 token!")
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
    
    print(">>>>>>>", file_path)

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