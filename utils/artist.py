import random

artist_list = [
    # 这边写上你喜欢的画师串
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
    "sho_(sho_lwlw)",
]


def get_random_artist():
    artist_num = random.randrange(5, 11)  # 抽取5个到10个画师
    random_selection = random.sample(artist_list, artist_num)
    random.shuffle(random_selection)
    _ = "artist:" + ",artist:".join(random_selection)
    print(f"抽取随机画师串 {_}")
    return _


if __name__ == "__main__":
    print(get_random_artist())
