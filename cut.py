from PIL import Image
import os
from tqdm import tqdm

# 源图片路径
source_path = input("请输入源图片路径:")

# 新文件夹路径
output_path = input("请输入新文件夹路径:")

# 创建新文件夹
os.makedirs(output_path, exist_ok=True)

# 获取源图片路径下的所有文件
files = [f for f in os.listdir(source_path) if f.endswith(".png")]

# 进度条
progress_bar = tqdm(total=len(files), desc="Processing images")

# 遍历源图片路径下的所有文件
for filename in files:
    # 加载图片
    image_path = os.path.join(source_path, filename)
    image = Image.open(image_path)

    # 裁剪底部100像素
    cropped_image = image.crop((0, 0, 832, 1116))

    # 生成新文件路径
    output_file = os.path.join(output_path, filename)

    # 保存裁剪后的图片到新文件夹
    cropped_image.save(output_file)

    # 关闭图片
    image.close()
    cropped_image.close()

    # 更新进度条
    progress_bar.update(1)
    progress_bar.set_postfix({"Remaining": len(files) - progress_bar.n})

# 关闭进度条
progress_bar.close()
