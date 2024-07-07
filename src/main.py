import pathlib
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageFont
import image
import os
import argparse
import json

import utils
import data
import config
from poster import Poster

# Get the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()


def main():
    doubaninfo = data.load_one_entry()

    # Create folder to save the poster image
    utils.create_folder()
    output_dir = current_dictionary / "../images"
    if config.delete_images:
        utils.delete_files_in_directory(output_dir)

    path = current_dictionary / "../assets/bgimage.png"
    successful = utils.save_image_from_url(doubaninfo.img_url, path)

    # Open the banner image
    if not successful:
        banned_entry_file_path = current_dictionary / "../assets/banned.json"
        with open(banned_entry_file_path, "r") as file:
            banned_titles = json.load(file)
        banned_titles.append(doubaninfo.title)
        with open(banned_entry_file_path, "w") as file:
            json.dump(banned_titles, file, ensure_ascii=False)
        banner = Image.new("RGB", (428, 623), color="white")
    else:
        banner = Image.open(path)

    # Create Poster object for drawing on the poster
    background_file_path = current_dictionary / "../assets/template.png"
    background = Image.open(background_file_path)
    font_light = f"../fonts/cn/LXGWWenKai-Light.ttf"
    rate = doubaninfo.rate
    mystery_poster = Poster(background, banner, font_light, rate)

    filename = "daily"
    utils.save_image_with_filename(mystery_poster.background, output_dir, filename)


if __name__ == "__main__":
    main()
