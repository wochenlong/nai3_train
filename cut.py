from PIL import Image
import os
from tqdm import tqdm

# 源图片路径
source_path = r""

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

    # 替换原图片
    image.close()
    os.remove(image_path)
    cropped_image.save(image_path)

    # 更新进度条
    progress_bar.update(1)
    progress_bar.set_postfix({"Remaining": len(files) - progress_bar.n})

# 关闭进度条
progress_bar.close()
