import os
import pathlib
from typing import Type, Tuple

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, TomlConfigSettingsSource

CONFIG_FILE = pathlib.Path(__file__).parent.parent / "config.toml"


class RunTimeSetting(BaseSettings):
    """
    运行时配置
    """
    token: str = Field(None, description="Novelai token")

    @field_validator("token")
    def check_token(cls, v):
        if v is None:
            raise ValueError("Token is required, 请在 .env 文件中配置 `TOKEN=xxx`")
        return v

    folder_path: str = Field("./images", description="Image save path")
    prompt_folder: str = Field("./prompts", description="Prompt folder path")
    characters_path: str = Field("./characters.json", description="Characters file path")

    prefix: str = Field("", description="Prefix for prompt")
    num_images: int = Field(1, description="Number of images to generate")
    batch_size: int = Field(1, description="Batch size")
    seed: int = Field(-1, description="Seed")
    negative_prompt: str = Field("", description="Negative prompt")

    sleep_time_batch_min: float = Field(10.0, description="Minimum sleep time between batches")
    sleep_time_batch_max: float = Field(20.0, description="Maximum sleep time between batches")
    sleep_time_single_min: float = Field(1.0, description="Minimum sleep time after single image")
    sleep_time_single_max: float = Field(5.0, description="Maximum sleep time after single image")
    retry_delay: float = Field(60.0, description="Retry delay")

    role_priority: int = Field(0, description="Role priority")
    read_mode: int = Field(-1, description="Read mode")

    artists: list[str] = Field([], description="Artists")
    artist_list: list[str] = Field([], description="Artist list")

    skip_pay_generate: bool = Field(False, description="Skip pay anlas")

    @field_validator("folder_path")
    def check_folder_path(cls, v):
        if not os.path.exists(v):
            os.makedirs(v)
        return v

    @field_validator("characters_path")
    def check_characters_path(cls, v):
        if not os.path.exists(v):
            raise FileNotFoundError(f"Characters file not found: {v}")
        return v

    @field_validator("prompt_folder")
    def check_prompt_folder(cls, v):
        if not os.path.exists(v):
            raise FileNotFoundError(f"Prompt folder not found: {v}")
        return v

    model_config = SettingsConfigDict(toml_file=CONFIG_FILE)

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


# 从环境变量中读取配置
env_var = RunTimeSetting()
