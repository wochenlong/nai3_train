from pathlib import Path
from PIL import Image


def read_prompt(img_path):
    r"""
    Read prompt using PIL form image produced by NAI3.
    """
    if isinstance(img_path, (str, Path)):
        img = Image.open(img_path)
    elif isinstance(img_path, Image.Image):
        img = img_path
    else:
        raise TypeError(f"Expected `str` or `Image`, got `{type(img_path)}`")

    description = img.info.get("Description")
    return description if description is not None else ""


def main():
    dir_p = Path(input("Enter directory path: "))
    if not dir_p.exists():
        raise FileNotFoundError(f"Directory `{dir_p}` does not exist.")
    for img_p in dir_p.glob("*.png"):
        prompt = read_prompt(img_p)
        cap_p = img_p.with_suffix(".txt")
        if cap_p.exists():
            print(f"Skipping `{img_p}`: caption already exists.")
            continue
        with open(cap_p, "w", encoding="utf-8") as f:
            if prompt is not None:
                f.write(prompt)
            else:
                f.write("")  # 写入一个空字符串
    print("Done.")


main()
