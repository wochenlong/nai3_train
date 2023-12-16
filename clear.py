import os
import random_prompt

output_path = "./output"

# 获取指定路径下所有的文件名
file_names = os.listdir(output_path)

for file_name in file_names:
    file_path = os.path.join(output_path, file_name)

    # 只处理文本文件
    if file_name.endswith(".txt"):
        with open(file_path, "r") as file:
            lines = file.readlines()

        with open(file_path, "w") as file:
            for line in lines:
                # 删除前缀相同的内容（包括逗号）
                if line.strip() != random_prompt.prefix:
                    file.write(line)

        print(f"已删除文件 {file_name} 中与前缀相同的内容")

print("处理完成")

