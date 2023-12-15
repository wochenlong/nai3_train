# nai3_train

nai3生成的图片，一键生成、打标和处理脚本

## 1. 批量生图，生成随机图片

必填参数：
- `self.token`：生图必需的token，授权令牌。获取方式如下：
  - 在网页中登录你的 NovelAI 账号
  - 打开控制台 (F12)，并切换到控制台 (Console) 标签页
  - 输入下面的代码并按下回车运行：
    ```javascript
    console.log(JSON.parse(localStorage.session).auth_token)
    ```
  - 输出的字符串就是你的授权令牌

- `prompt_folder`：从这个文件夹里面随机抽取TXT，作为提示词
- `negative_prompt`：负面提示词
- `num_images`：生成图片的总数量
- `batch_size`：每批次生成的图像数量
- `sleep_time`： 每批次生成后的休眠时间（单位：秒）

运行命令：`Python random_prompt`

## 2. 读取图片信息，并生成txt同名文件

运行命令：`Python tagger.py`

然后按提示输入要处理的文件夹路径即可

## 3. 去掉txt文件中的非法字符，比如😄🙃

运行命令：`Python UTF-8.py`

请注意，以上命令中的`Python`指的是运行Python解释器的命令，具体的命令可能因你的操作系统和Python安装方式而有所不同。请根据你的实际情况进行相应的调整。
