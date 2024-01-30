from itertools import product

# 定义艺术家和括号的列表
artists = [
    "artistA",
    "artistB",
    "artistC",
    "artistD",
    "artistE",
    "artistF",
    "artistG",
    "artistH",
    "artistI",
    "artistJ",
]
brackets = ["[]", "{}"]

# 创建一个空列表用于存储所有可能的组合
combinations = []

# 根据艺术家数量生成所有可能的括号组合
for combo in product(brackets + [""], repeat=len(artists)):
    combination = ", ".join(
        [f"{b[0]}{a}{b[1]}" if b != "" else a for a, b in zip(artists, combo)]
    )
    combinations.append(combination)

# 打印所有可能的组合
print("所有可能的组合：")
for combination in combinations:
    print(combination)

# 打印总共生成的组合数量
print("总共有", len(combinations), "种组合。")
import random
from itertools import product

# 定义艺术家和括号的列表
artists = [
    "artistA",
    "artistB",
    "artistC",
    "artistD",
    "artistE",
    "artistF",
    "artistG",
    "artistH",
    "artistI",
    "artistJ",
]
brackets = ["[]", "{}"]

# 创建一个空列表用于存储所有可能的组合
combinations = []

# 根据艺术家数量生成所有可能的括号组合
for combo in product(brackets + [""], repeat=len(artists)):
    combination = ", ".join(
        [f"{b[0]}{a}{b[1]}" if b != "" else a for a, b in zip(artists, combo)]
    )
    combinations.append(combination)

# 随机选择 N 个组合
N = 2
random_combinations = random.sample(combinations, N)

# 打印随机选择的组合
print(f"随机选择的 {N} 种组合：")
for combination in random_combinations:
    print(combination)

# 打印总共生成的组合数量
print("总共有", len(combinations), "种组合。")
