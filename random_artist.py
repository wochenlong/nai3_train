import asyncio

from app.request import NovelaiInspire, GenerateMode, generate
from app.settings import env_var


async def main():
    generator = NovelaiInspire(
        generate_mode=GenerateMode.RANDOM_ARTIST,
        prompt_folder=env_var.prompt_folder,
        artists=env_var.artists,
    )
    # 创建 NovelaiImageGenerator 实例
    await generate(generator=generator)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
