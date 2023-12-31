# nai3_train

If you need to use the images generated by nai3 to train your SD model in batches, then I believe you need this project.

The nai3-generated images are generated, labeled, and processed with a single script.

Principle: Randomly select a .txt file from the `prompt_folder` as a prompt to generate random materials in batches.

Note: If there is no pressure to update, there won't be any updates. The `clear.py` script has some issues, it can only remove keywords but not commas.

## Open Source Random Prompt Word Library
A massive collection of random prompt words in .txt format. After extracting, place them in the `prompt_folder`.

1. 4K High-Quality Prompt Word Library: [Download](https://huggingface.co/datasets/windsingai/random_prompt/resolve/main/prompt_4k.zip)
   - Features: Manually curated, high-quality, high safety rating with only 2% NSFW content.
   - Content: Mainly focused on characters and composition.
   - Source: Modified from the labeled files of the AID training set by Yugi.

2. 200K High-Quality Prompt Word Library: [Download](https://huggingface.co/datasets/windsingai/random_prompt/resolve/main/prompt_20W.zip)
   - Features: Reverse-engineered from real images, large quantity, high concentration of 2D content, sufficient generalization, approximately 20% NSFW content.
   - Content: Diverse themes, considering the composition of Danbooru, predominantly female-focused.
   - Source: Batch crawled from [https://danbooru.donmai.us/](https://danbooru.donmai.us/) and modified from the 200K training set by GangGangGe.

## 1. Batch Image Generation - Generating Random Images

Required Parameters:
- `self.token`: Token required for image generation, authorization token. Obtain it as follows:
  - Log in to your NovelAI account on the website ([https://novelai.net](https://novelai.net)).
  - Open the console (F12) and switch to the Console tab.
  - Enter the following code and press Enter:
    ```javascript
    console.log(JSON.parse(localStorage.session).auth_token)
    ```
  - The output string is your authorization token.

- `prompt_folder`: Randomly extract TXT files from this folder as prompts.
- `prefix`: Default prefix, customized quality words or fixed artist styles.
- `negative_prompt`: Negative prompt words.
- `num_images`: Total number of generated images.
- `batch_size`: Number of images generated per batch.
- `sleep_time`: Sleep time after each batch generation (in seconds).
- `retry_delay`: Time for the script to automatically restart after encountering an exception (in seconds).

Command to run: `Python random_prompt`

## 2. Read Image Information and Generate TXT Files with the Same Names

Command to run: `Python nai3tagger.py`

Then enter the folder path you want to process as prompted.

## 3. Remove the Prefix `prefix` from the TXT Files and Bind the Art Style

Command to run: `Python clear.py`

## 4. Remove Illegal Characters from the TXT Files, such as 😄🙃

Command to run: `Python UTF-8.py`
