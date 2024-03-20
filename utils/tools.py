import os


def get_token():
    file_path = "./token.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            token = file.read()
            return token
    else:
        token_input = input("请输入你从网页获取的token：")
        with open(file_path, "w") as file:
            file.write(token_input)
        return token_input
