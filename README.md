# ✨ nai3_train ✨

英文版本指南：[English Documentation](./README_EN.md)

如果你需要批量训练你的SD模型并使用 nai3 生成的图片，那么你会发现这个项目非常有用。

nai3 是一个帮助你批量生成、标记和处理图片的一键式脚本工具。

操作原理1：脚本从 `prompt_folder` 文件夹中随机取样文本作为提示，然后批量生成随机素材。

你可以把你的标注文本(responses)文件转化为一个随机提示词库！

操作原理2：脚本从 json 文件中随机抽取角色以生成随机角色，或者按照一定的顺序生成所有角色。

备注：我们欢迎你提出新功能需求，脚本仍在持续优化开发中。

## 💿 安装运行环境

```bash
pip install pdm
# 自动创建虚拟环境并锁定依赖版本
pdm install
```

## ⚙️ 配置

你需要通过文本编辑器（如记事本等）打开同级目录下的 `config.toml` 文件，并按照注释进行个性化配置。其中 **token** 是必需配置的项目，其他配置项可以保持默认。

获取 token 的方法：

- 在网页端（https://novelai.net） 登录你的 NovelAI 账号。
- 在左上角个人中心找到 "Account"。
- 在 "Get Persistent API Token." 栏目下。
- 点击 "Generate Token" 按钮生成 token。

## ✨ 支持的主要采样器列表

采样器包括：
```
"k_euler",
"k_euler_ancestral",
"k_dpmpp_2s_ancestral",
"k_dpmpp_2m",
"k_dpmpp_sde",
"ddim_v3",
```

## ✨ 生成的随机角色效果：

图一

![VA}S0W4AL6_ZIV~2 (BDX5](https://github.com/wochenlong/nai3_train/assets/117965575/6bfecd63-fa7f-4b36-bef9-1e8df2eef21f)

图二

![0~O)3% YX{SRSL$2VY)PTJ](https://github.com/wochenlong/nai3_train/assets/117965575/093c08fc-bf83-4d38-a282-7470bf48e316)

图三：

![L_ZUGFLNWQXDY~4(A4~5XK2](https://github.com/wochenlong/nai3_train/assets/117965575/711aff18-3ef7-4390-889e-c0ffc846418e)

图四：

![V2L6B62X60RU7((XCBMAN 9](https://github.com/wochenlong/nai3_train/assets/117965575/7b290ae4-5d77-4210-9276-519bd8afe6d6)

## ✨ 生成的随机素材效果：

图四：

![8R@KZV(13`(0U~25~KKQTR7](https://github.com/wochenlong/nai3_train/assets/117965575/1c5a42bf-b44e-48a6-aaab-aa5487554a42)

图五：

![N9 KXF41KXXB2T~CKZ2VS`M](https://github.com/wochenlong/nai3_train/assets/117965575/37e1801f-bfea-4f7c-8701-ed4047c29a28)

## 🤗 开源随机提示词库

我们提供了海量的 txt 文件格式的随机提示词供你使用。只需将解压后的文件放入 `prompt_folder` 即可。

| 图库 | 4K 高质量                      | 20W 高质量                                             |
|----|-----------------------------|-----------------------------------------------------|
| 特点 | 人工整理，良品率高，安全性高，只有 2% 的 NSFW | 真实图片反推，数量多，二次元浓度高，泛化性高，大约有 20% 的 NSFW               |
| 内容 | 主要是人物和构图为主                  | 题材丰富，但受到 danbooru 的主题影响，主要以女性为主                     |
| 来源 | 修改自尤吉的AID训练集的标记文件           | 从 https://danbooru.donmai.us/ 批量爬取和修改，来源于杠杠哥的20W训练集 |

## 🎉 快速入门

### 1️⃣ random_characetrs.py

随机或按顺序生成指定角色的图片

这个脚本通过读取 json 文件中的角色名来生成图片。我们提供了内置的随机角色库，包含原神、明日方舟、FGO 等主流游戏的角色。

例如，你可以通过读取.\json\genshin.json 文件，实现随机原神角色生成。

genshin.json 的文件结构如下：

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

### 2️⃣ random_prompt.py

这个脚本可以读取随机提示词库，批量生成随机 nai3 图片。

### 3️⃣ nai3tagger.py

读取图片信息，并生成与图片同名的 txt 文件。

### 4️⃣ clear.py

去掉 txt 文件中的前缀 `prefix` ，用于绑定画风。

### 5️⃣ UTF-8.py

去掉 txt 文件中的非法字符，例如😄🙃。 一些非法字符可能导致在进行模型训练时报错，因此必须将这些字符去除。

### 6️⃣ cut.py

去掉图片中的水印。