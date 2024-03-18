import random
import requests
import zipfile
import io
import json
import zipfile

from utils.utils import *



class NovelaiImageGenerator:
    def __init__(self, characters_path):
        self.token = token
        self.api = "https://api.novelai.net/ai/generate-image"
        self.headers = headers
        self.json = json_

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

    def generate_image(self, prefix, random_mode=True, seed=None):
        if seed is None or seed == -1:
            seed = random.randint(0, 9999999999)
        self.json["parameters"]["seed"] = seed

        if random_mode:
            random_character = self.get_random_character()
        else:
            random_character = self.get_next_character()

        if env_vars["role_priority"] == 1:
            random_character = self.get_random_character()
            self.json["input"] = random_character + prefix
        else:
            self.json["input"] = prefix + random_character

        r = requests.post(
            self.api, json=self.json, headers=self.headers
        )  # 将这行移动到这里，确保任何情况下都会执行
        with zipfile.ZipFile(io.BytesIO(r.content), mode="r") as zip:
            with zip.open("image_0.png") as image:
                return image.read()



generator = NovelaiImageGenerator(characters_path=env_vars["characters_path"])

# 加载角色列表
generator.load_characters()

# 生成并保存图像
image_data = generator.generate_image("prefix_", random_mode=(env_vars["read_mode"] == -1))

save_image_from_binary(image_data, "image_folder")

generate(generator)