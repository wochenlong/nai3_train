import gradio as gr
from random_artist_weight import _ARTISTS
from random_characetrs_expression import NovelaiImageGenerator, save_image_from_binary
import random
import time
import zipfile
from tqdm import tqdm
from requests.exceptions import SSLError, RequestException
import sys
import webbrowser


def gen_random_char(characters_path, expressions_path, folder_path, prefix, negative_prompt, i_random, num_images, batch_size):
    generator = NovelaiImageGenerator(
        characters_path=characters_path, negative_prompt=negative_prompt, expressions_path=expressions_path
    )

    generator.load_characters()
    generator.load_expressions()

    for i in tqdm(range(num_images)):
        try:
            # 生成图像数据
            image_data = generator.generate_image(prefix, random_mode=i_random)
            if image_data is None:
                continue

            # 保存图像文件
            save_image_from_binary(image_data, folder_path)

            if (i + 1) % batch_size == 0:  # 批次执行结束休眠
                sleep_time = (
                        random.uniform(100, 300)
                        / 100.0
                )
                print(f"已生成 {i + 1} 张图像，休眠 {sleep_time} 秒...")
                time.sleep(sleep_time)
            else:  # 单次执行完后休眠
                sleep_time = (
                        random.uniform(50, 300)
                        / 100.0
                )
                print(f"图像生成完毕，休眠 {sleep_time} 秒...")
                time.sleep(sleep_time)
        except (SSLError, RequestException) as e:
            print("发生错误:", e)
            print(f"休眠2秒后重新启动")
            time.sleep(2)
        except zipfile.BadZipFile as e:
            print("发生错误:", e)
            print("忽略此错误，继续脚本运行")


with gr.Blocks() as iblock:
    with gr.Tab("生图"):
        char_path_input = gr.Textbox(label="角色文件夹路径", value=r".\json\genshin.json")
        exp_path_input = gr.Textbox(label="表情文件夹路径", value=r".\json\arknights_ge_50.json")
        output_path_input = gr.Textbox(label="输出文件夹路径", value=r".\output")
        prefix_input = gr.Textbox(label="固定画风", value="naga_u,[tyakomes],henreader,baku-p,year_2023,official art,1girl,portrait,lineart,monochrome,solo,portrait,white background, simple background, upper body,{{cropped shoulders}}, looking at viewer, hair highlight, light eyes")
        negative_prompt_input = gr.Textbox(label="负面提示词", value="nsfw,ugly,coat,lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], lowres, {bad}, error, fewer, extra,missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan")
        is_random = gr.Checkbox(label="随机顺序", value=True)
        seed_input = gr.Textbox(label="随机种子", value='', placeholder='无效')
        num_input = gr.Slider(minimum=1, maximum=999, step=1, label="生成数量", value=20)
        bs_input = gr.Slider(minimum=1, maximum=100, step=1, label="生成批次", value=10)
        output = gr.Textbox(label="运行结果")
        gen_button = gr.Button(label="生成")
    gen_button.click(gen_random_char, [char_path_input, exp_path_input, output_path_input, prefix_input, negative_prompt_input, is_random, num_input, bs_input], [output])
    iblock.title = "webui"
if sys.platform == "win32":
    webbrowser.open('http://127.0.0.1:7864')
iblock.launch(server_port=7864)
