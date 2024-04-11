import os
from io import BytesIO

from novelai_python.tool.image_metadata import ImageMetadata

# 源图片路径
source_path = input("请输入源图片路径:")
# 新文件夹路径
output_path = input("请输入新文件夹路径:")
# 创建新文件夹
os.makedirs(output_path, exist_ok=True)
# 获取源图片路径下的所有文件
files = [f for f in os.listdir(source_path) if f.endswith(".png")]

# 遍历源图片路径下的所有文件
for filename in files:
    # 读取文件后调用 ImageMetadata.reset_alpha() 方法，然后写回文件
    with open(os.path.join(source_path, filename), "rb") as f:
        reset = ImageMetadata.reset_alpha(BytesIO(f.read()))
        output_file = os.path.join(output_path, filename)
        # 保存裁剪后的图片到新文件夹
        with open(output_file, "wb") as out:
            out.write(reset.getvalue())
