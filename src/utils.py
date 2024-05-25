"""
This module provides functionalities related to interacting with the Spotify API.

Imports:
    - re: Module for regular expressions used in string manipulation.
    - os: Module for interacting with the operating system.
    - datetime: Module for working with dates and times.
    - pathlib: Module for working with filesystem paths.
    - print: Function from the rich library for enhanced output formatting.
    - Language, LanguageDetectorBuilder: Classes from the lingua library for language detection.
"""

import re
import os
import datetime
import pathlib
from PIL import Image
import locale
from pybadges import badge
from io import BytesIO
import cairosvg
import random
import urllib

from rich import print
from lingua import Language
from lingua import LanguageDetectorBuilder


def decide_font(text: str, weight: int):
    """
    Determines the font to use based on the text and font weight.

    Args:
        text (str): The text to analyze for language detection.
        weight (int): The weight of the font.

    Returns:
        str: The path to the selected font file.
    """
    path = "../fonts/"

    lang = {
        "en": "Oswald/Oswald",
        "ko": "NotoSansKR/NotoSansKR",
        "ja": "NotoSansJP/NotoSansJP",
        "zh": "NotoSansTC/NotoSansTC",
    }

    variant = ["ExtraLight", "Light", "Regular", "Medium", "Semibold", "Bold"]

    # Language detection
    detector = LanguageDetectorBuilder.from_languages(
        Language.ENGLISH, Language.KOREAN, Language.JAPANESE, Language.CHINESE
    ).build()
    detected = str(detector.detect_language_of(text).iso_code_639_1.name).lower()

    # Construct font path
    font = f"{path}{lang[detected]}-{variant[weight]}.tff"

    return font


def create_image(width, height):
    color = (255, 255, 255)
    image = Image.new("RGB", (width, height), color)
    return image


def convert_to_japanese(day):
    days_dict = {
        "Monday": "月曜日",
        "Tuesday": "火曜日",
        "Wednesday": "水曜日",
        "Thursday": "木曜日",
        "Friday": "金曜日",
        "Saturday": "土曜日",
        "Sunday": "日曜日",
    }

    return days_dict.get(day, "Invalid day")


def print_date_cn():
    # do not work on github action
    # locale_format = "zh_CN.UTF-8"
    # locale_format = "ja_JP.UTF-8"
    locale_format = "en_US.UTF-8"
    locale.setlocale(locale.LC_ALL, locale_format)

    # Get the current date
    current_date = datetime.datetime.now()

    # Format and print the date
    formatted_date = current_date.strftime("%m月%d日 | %A")

    formatted_date = formatted_date.split("|")
    formatted_date = (
        formatted_date[0] + " | " + convert_to_japanese(formatted_date[1].strip())
    )

    return formatted_date


def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"{file_path} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def create_folder():
    """
    Creates a folder named 'images' if it doesn't exist.

    Prints a message indicating the creation of the folder.
    """
    cur = pathlib.Path(__file__).parent.resolve()
    if not os.path.exists(cur / "../images/"):
        os.makedirs(cur / "../images/")
        print(
            "[📦] Created a folder called "
            "[bold underline turquoise4]../images[/bold underline turquoise4] "
            "outside of this directory for output."
        )


def special_code():
    """
    Generates a special code based on the current timestamp.

    Returns:
        int: The generated special code.
    """
    return ((int(datetime.datetime.now().timestamp()) % 10000) + 10000) % 10000


def create_filename(song, artist):
    """
    Creates a safe filename based on the song and artist names.

    Args:
        song (str): The name of the song.
        artist (str): The name of the artist.

    Returns:
        str: The safe filename.
    """
    full_text = f"{song} by {artist}"
    safe_text = (
        re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', "_", full_text)
        .strip()
        .strip(".")
        .lower()
        .replace(" ", "_")
    )
    safe_text = re.sub(r"_{2,}", "_", safe_text)
    return safe_text[:255]


def draw_on_poster(top, left, poster, banner):
    right = left + banner.width
    bottom = top + banner.height
    box = (left, top, right, bottom)

    # Paste the banner image onto the poster
    poster.paste(banner, box)


def create_badge(color, website, score):
    svg_data = badge(
        left_text=website, right_text=score, left_color=color, right_color="blue"
    )
    png_data = cairosvg.svg2png(bytestring=svg_data)
    svg_image = Image.open(BytesIO(png_data))

    scale = 3
    new_size = (svg_image.width * scale, svg_image.height * scale)
    svg_image = svg_image.resize(new_size)
    return svg_image


def resize_image(img, max_size=1000):
    # Get the dimensions
    width, height = img.size

    # Calculate the aspect ratio
    aspect_ratio = 428 / 623

    # Calculate the new dimensions
    new_height = max_size
    new_width = int(max_size * aspect_ratio)

    # Resize the image
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return resized_img


def save_image_from_url(url, save_path):
    successful = True

    agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
    ]
    headers = {"user-agent": random.choice(agents)}

    req = urllib.request.Request(url, headers=headers)
    content = urllib.request.urlopen(req)
    if content.status != 200:
        return False
    content = content.read()

    # Open the image using PIL
    output = BytesIO(content)
    img = Image.open(output)
    # Save the image to the specified path
    img.save(save_path)
    print("Image saved successfully at:", save_path)
    successful = True

    return successful


def save_image_with_filename(img, output_dir, filename):
    output_path = os.path.join(output_dir, f"{filename}.png")
    # Save the poster image
    img.save(output_path, quality=100)
    # print(f"[☕] Image saved to {output_path}")
