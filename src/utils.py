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