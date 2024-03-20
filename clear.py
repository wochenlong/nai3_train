import os

prefix = input("请输入你的画师词/质量词:")  # 你的画师词/质量词

dirpath = input("请输入要处理的文件夹路径:")  # 要处理的文件夹路径


# 遍历指定目录下的文件
for filename in os.listdir(dirpath):
    # 只处理以".txt"结尾的文件
    if filename.endswith(".txt"):
        # 打开文件进行读取
        with open(os.path.join(dirpath, filename), "r") as f:
            # 读取文件内容
            caption = f.read()
            # 替换不需要的词语
            caption = caption.replace(prefix, "")
        # 打开文件进行写入
        with open(os.path.join(dirpath, filename), "w") as f:
            # 写入修改后的内容
            f.write(caption)

# 执行完毕后提醒用户
print("当前画风词/质量词已成功去除")
