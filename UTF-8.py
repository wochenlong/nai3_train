import os
import shutil


def move_files_with_non_utf8_encoding(directory, destination):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        f.read()
                except UnicodeDecodeError:
                    # 文件包含非 UTF-8 编码字符
                    # 移动txt文件
                    shutil.move(file_path, os.path.join(destination, file))

                    # 移动同名的图片文件
                    image_file = os.path.splitext(file)[0] + ".png"  # 假设图片文件扩展名为.jpg
                    image_path = os.path.join(root, image_file)
                    if os.path.exists(image_path):
                        shutil.move(image_path, os.path.join(destination, image_file))


# 指定含有非 UTF-8 编码字符的文件所在目录
directory_path = r"E:\waifuc\data\tutu\10_tu"

# 指定目标文件夹路径，用于存放移动后的文件
destination_path = r"E:\waifuc\data\tutu\destination"

# 移动含有非 UTF-8 编码字符的文件到目标文件夹
move_files_with_non_utf8_encoding(directory_path, destination_path)
