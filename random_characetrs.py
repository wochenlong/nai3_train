import asyncio

from app.request import NovelaiInspire, GenerateMode, generate
from app.settings import env_var


async def main():
    generator = NovelaiInspire(
        generate_mode=GenerateMode.RANDOM_CHARACTER,
        prompt_folder=env_var.prompt_folder,
        characters=NovelaiInspire.load_characters_from_file(characters_path=env_var.characters_path)
    )
    # 创建 NovelaiImageGenerator 实例
    await generate(generator=generator)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
