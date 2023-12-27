
#  nai3_train
英文版说明：[English Documentation](./README_EN.md)

如果你需要使用nai3生成的图片来批量训练你的SD模型，那我想你需要这个项目。

nai3生成的图片，一键生成、打标和处理脚本

原理：从prompt_folder随机抽取txt作为prompt批量生成随机素材

备注：不催更就不更新，clear.py脚本 有些问题，只能去掉关键词，不能去掉  ， 号

## 开源随机提示词库
海量txt随机提示词，解压后放进`prompt_folder`即可。

一、 4K高质量提示词库 ：https://huggingface.co/datasets/windsingai/random_prompt/resolve/main/prompt_4k.zip

 特点：人工整理，良品率高，安全性高，只有2%的nsfw

 内容：以人物和构图为主

 来源：修改自尤吉的AID训练集的打标文件

二、 20w高质量提示词库 ：https://huggingface.co/datasets/windsingai/random_prompt/resolve/main/prompt_20W.zip

  特点：真实图片反推，数量多，二次元浓度高，足够泛化，约有20%的nsfw

  内容：题材很多，考虑到danbooru的构成，主要还是以女性为主
  
  来源：从 https://danbooru.donmai.us/ 批量爬取，修改自杠杠哥的20W训练集
 
 



## 1. 批量生图，生成随机图片

必填参数：
- `self.token`：生图必需的token，授权令牌。获取方式如下：
  - 在网页（https://novelai.net） 中登录你的 NovelAI 账号
  - 打开控制台 (F12)，并切换到控制台 (Console) 标签页
  - 输入下面的代码并按下回车运行：
    ```javascript
    console.log(JSON.parse(localStorage.session).auth_token)
    ```
  - 输出的字符串就是你的授权令牌

- `prompt_folder`：从这个文件夹里面随机抽取TXT，作为提示词
- `prefix`：默认前缀，自定义的质量词或者固定的画家风格
- `negative_prompt`：负面提示词
- `num_images`：生成图片的总数量
- `batch_size`：每批次生成的图像数量
- `sleep_time`： 每批次生成后的休眠时间（单位：秒）
- `retry_delay`： 脚本遇到异常中断后，重新自动启动的时间（单位：秒）

运行命令：`Python random_prompt`

## 2. 读取图片信息，并生成txt同名文件

运行命令：`Python nai3tagger.py`

然后按提示输入要处理的文件夹路径即可

## 3. 去掉txt文件中的前缀`prefix` ，绑定画风

运行命令：`Python clear.py`

## 4. 去掉txt文件中的非法字符，比如😄🙃

运行命令：`Python UTF-8.py`

