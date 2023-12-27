
#  nai3_train
英文版说明：[English Documentation](./README_EN.md)

如果你需要使用nai3生成的图片来批量训练你的SD模型，那我想你需要这个项目。

nai3生成的图片，一键生成、打标和处理脚本

原理1：从prompt_folder随机抽取txt作为prompt批量生成随机素材

   把你的打标txt变成你的随机提示词库！

原理2：从json中随机抽取角色生成随机角色，或者按顺序生成所有角色

备注：不催更就不更新，clear.py脚本 有些问题，修复中
# 生成的随机角色效果：
图一

![VA}S0W4AL6_ZIV~2 (BDX5](https://github.com/wochenlong/nai3_train/assets/117965575/6bfecd63-fa7f-4b36-bef9-1e8df2eef21f)

图二

![0~O)3% YX{SRSL$2VY)PTJ](https://github.com/wochenlong/nai3_train/assets/117965575/093c08fc-bf83-4d38-a282-7470bf48e316)







# 生成的随机素材效果：

![`JLI)UOF4 9_ W4GL ~VHH9](https://github.com/wochenlong/nai3_train/assets/117965575/37d81ffd-66c7-4931-81d7-8b2a018138d3)



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
 
 
## 新功能： 随机/按顺序生成指定角色的图片

原理，从json读取角色名，生成图片

本仓库内置genshin.json和arknights_ge_50.json 文件

例：
使用通过读取.\json\genshin.json 文件，实现随机原神角色生成。

使用通过读取.\arknights_ge_50.json 文件，实现随机方舟角色生成，arknights_ge_50.json收录了在danbooru有50张图以上的方舟角色。


json文件的结构，以genshin.json为例：

```
{
  "role": [
    "noelle_(genshin_impact)",
    "faruzan_(genshin_impact)",
    "角色1",
    "角色2",
    "角色3",
    .....
  ]
```

下面为random_characetrs.py脚本的部分代码：
```

# 用户自定义 角色 JSON 文件的路径
characters_path = "./json/arknights_ge_50.json"
# 生成图像文件的保存路径
folder_path = ".\output"
# 选择读取方式
read_mode = 1  # -1为随机读取，1为按顺序读取
# 设置角色优先级
role_priority = 1  # 默认为不生效,选择1时，把角色词优先放prefix 前面
# 选择 seed
seed = 6666  # 默认随机 seed，不填或者设置为-1时为随机seed

# 生成多张图像并保存
num_images = 200  # 要生成的图像数量
batch_size = 10  # 每批次生成的图像数量
retry_delay = 20  # 每批次生成后的休眠时间（单位：秒）

sleep_time = 10  # 每批次生成后的休眠时间（单位：秒）

retry_delay = 60  # 因为报错中断，脚本的重新启动时间（单位：秒）
prefix = "official art,cowboy shot,standing,white background, "  # 加在提示词前面的固定画风词或质量词

class NovelaiImageGenerator:
    def __init__(self, characters_path, negative_prompt):
        self.token = "xxx" # 请自行获取
....

```
参数说明：
- `self.token`：生图必需的token，授权令牌。获取方式如下：
  - 在网页（https://novelai.net） 中登录你的 NovelAI 账号
  - 打开控制台 (F12)，并切换到控制台 (Console) 标签页
  - 输入下面的代码并按下回车运行：
    ```javascript
    console.log(JSON.parse(localStorage.session).auth_token)
    ```
  - 输出的字符串就是你的授权令牌
- `characters_path`： 角色 JSON 文件的路径，从这个 JSON随机抽取角色生成
- `read_mode `：选择读取json里面的角色的方式，-1为随机读取，1为按顺序读取
- `prefix`：默认前缀，自定义的质量词或者固定的画家风格
- `role_priority`：设置角色优先级，默认不生效，当选择1时，把角色词优先放prefix前面
- `seed`：种子，默认随机 seed，不填或者设置为-1时为随机seed
- `negative_prompt`：负面提示词
- `num_images`：生成图片的总数量
- `batch_size`：每批次生成的图像数量
- `sleep_time`： 每批次生成后的休眠时间（单位：秒）
- `retry_delay`： 脚本遇到异常中断后，重新自动启动的时间（单位：秒）

运行命令：`Python random_characetrs.py`




## 1. 读取随机提示词库，批量生成随机nai3图片

以下为 random_prompt.py脚本的部分代码

```
...
class NovelaiImageGenerator:
    def __init__(self, prompt_folder, negative_prompt):
        # 初始化函数，接受两个参数：prompt_folder 和 negative_prompt
   self.token = "xxx"  # 设置 API 的访问令牌
...

# 创建 NovelaiImageGenerator 实例
generator = NovelaiImageGenerator(
    prompt_folder=".\prompt",
    negative_prompt=" nsfw, lowres, ",
)

# 生成图像文件的保存路径
folder_path = ".\output"

# 生成多张图像并保存
num_images = 1000  # 要生成的图像数量
batch_size = 10  # 每批次生成的图像数量
retry_delay = 20  # 每批次生成后的休眠时间（单位：秒）

sleep_time = 10  # 每批次生成后的休眠时间（单位：秒）

retry_delay = 60  # 因为报错中断，脚本的重新启动时间（单位：秒）
prefix = "amazing quality, absurdres, year 2023, " 默认前缀 



```

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

