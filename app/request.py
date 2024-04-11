import asyncio
import os
import random
import re
import sys
import unicodedata
from enum import Enum
from typing import List

import shortuuid
from loguru import logger
from novelai_python import GenerateImageInfer, ApiCredential, APIError, AuthError
from pydantic import BaseModel, model_validator, SecretStr

from app.settings import env_var

credential = ApiCredential(api_token=SecretStr(env_var.token))

try:
    import ujson as json
except ImportError:
    import json

logger.remove(0)
handler_id = logger.add(
    sys.stderr,
    format="<level>[{level}]</level> | <level>{message}</level> | <yellow>@{time}</yellow>",
    colorize=True,
    backtrace=True,
    enqueue=True,
    level="INFO" if not os.getenv("DEBUG") else "DEBUG"
)


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class GenerateMode(Enum):
    RANDOM_ARTIST = 1
    RANDOM_CHARACTER = 2
    RANDOM_PROMPT = 3


class NovelaiInspire(BaseModel):
    generate_mode: GenerateMode
    prompt_folder: str
    artists: List[str] = []
    characters: List[str] = []
    current_character_index: int = 0

    @model_validator(mode="after")
    def check_after_init(self):
        # 判定prompt_folder是否存在，是否是文件夹
        if not os.path.exists(self.prompt_folder) or not os.path.isdir(self.prompt_folder):
            raise ValueError(f"Prompt folder not found: {self.prompt_folder}")

    @staticmethod
    def load_characters_from_file(characters_path):
        try:
            with open(characters_path, "r") as file:
                data = json.load(file)
                return data["role"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Characters file load failed: {characters_path} because {e}")

    def get_random_character(self):
        character = random.choice(self.characters)
        logger.info(f"抽取随机角色串 {character}")
        return character

    def get_random_artist(self):
        artist_num = random.randrange(5, 11)  # 抽取5个到10个画师
        random_selection = random.sample(self.artists, artist_num)
        random.shuffle(random_selection)
        _ = "artist:" + ",artist:".join(random_selection)
        logger.info(f"抽取随机画师串 {_}")
        return _

    def get_next_character(self):
        character = self.characters[self.current_character_index]
        self.current_character_index = (self.current_character_index + 1) % len(
            self.characters
        )
        logger.info(f"抽取随机角色串 {character}")
        return character

    async def _generate_image(self, prefix):
        prompt_file = random.choice(os.listdir(self.prompt_folder))
        prompt_file_path = os.path.join(self.prompt_folder, prompt_file)
        with open(prompt_file_path, "r") as file:
            random_prompt = file.read()
        if env_var.seed == -1:
            env_var.seed = random.randint(0, 4294967288)

        if self.generate_mode == GenerateMode.RANDOM_ARTIST:
            str_artist = self.get_random_artist()
            prompt = f"{str_artist},{prefix}"
        elif self.generate_mode == GenerateMode.RANDOM_CHARACTER:
            if env_var.read_mode:
                random_character = self.get_random_character()
            else:
                random_character = self.get_next_character()
            if env_var.role_priority == 1:
                prompt = random_character + prefix
            else:
                prompt = prefix + random_character
        elif self.generate_mode == GenerateMode.RANDOM_PROMPT:
            prompt = prefix + random_prompt
        else:
            raise ValueError("Invalid Mode")
        gen = GenerateImageInfer.build(
            prompt=prompt,
            seed=env_var.seed,
            negative_prompt=env_var.negative_prompt,
            ucPreset=0,
        )
        cost = gen.calculate_cost(is_opus=True)
        if env_var.skip_pay_generate and cost != 0:
            logger.info(f"跳过付费生成: {prompt},vip3 cost: {cost}")
            return None, prompt
        logger.info(f"生成图像: {prompt},vip3 cost: {cost}")
        result = await gen.request(session=credential)
        return result, prompt

    async def generate_images(self, prefix, save_folder: str):
        try:
            result, prompt = await self._generate_image(prefix)
            if result is None:
                return
            for file in result.files:
                _, filebytes = file
                filename = slugify(f"{prompt[:15]}_{shortuuid.uuid()[:2]}")
                file_path = os.path.join(save_folder, f"{filename}.png")
                with open(file_path, "wb") as f:
                    f.write(filebytes)
                logger.info(f"图像已保存到：{file_path}")
        except AuthError as e:
            logger.error(f"鉴权失败 {e.message}")
            raise e
        except APIError as e:
            logger.error(f"Request Api error: {e.message}")
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")


async def generate(generator: NovelaiInspire):
    try:
        for i in range(int(env_var.num_images)):
            await asyncio.sleep(0.1)
            await generator.generate_images(env_var.prefix, env_var.folder_path)
            if (i + 1) % int(env_var.batch_size) == 0:
                sleep_time = (
                        random.uniform(float(env_var.sleep_time_batch_min) * 100,
                                       float(env_var.sleep_time_batch_max) * 100)
                        / 100.0
                )
                logger.info(f"已生成 {i + 1} 张图像，休眠 {sleep_time} 秒...")
                await asyncio.sleep(sleep_time)
            else:
                sleep_time = (
                        random.uniform(float(env_var.sleep_time_single_min) * 100,
                                       float(env_var.sleep_time_single_max) * 100)
                        / 100.0
                )
                logger.info(f"图像生成完毕，休眠 {int(sleep_time)} 秒...")
                await asyncio.sleep(int(sleep_time))
    except AuthError as e:
        logger.error(f"请你配置正确的密钥 `pst-****`\n{e.message}")
        raise e
    except Exception as e:
        logger.error("Unhandled exception:", e)
        logger.info(f"休眠 {env_var.retry_delay} 秒后重新启动")
        # 休眠 retry_delay 秒后重新启动
        await asyncio.sleep(env_var.retry_delay)
