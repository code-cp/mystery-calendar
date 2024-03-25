from PIL import Image
from io import BytesIO
import pathlib
from datetime import datetime
import json
import random
from dataclasses import dataclass
import textwrap
from typing import *

current_dictionary = pathlib.Path(__file__).parent.resolve()


@dataclass
class DoubanInfo:
    id: str
    img_url: str
    title: str
    rate: str
    review: str
    category: str
    date: str
    is_movie: bool
    color: List[Any]


current_dictionary = pathlib.Path(__file__).parent.resolve()


def format_date(date_str):
    formatted_date = date_str.split("(")[0]
    return formatted_date

def check_word_in_sentence(word_list, sentence):
    for word in word_list:
        if word in sentence:
            return True
    return False


def load_one_entry():
    file_path = current_dictionary / "../data/douban/"  # Path to your JSON file

    my_type = "movie" if random.random() < 0.5 else "book"
    is_movie = True if my_type == "movie" else False 
    file_path = file_path / f"{my_type}.json"

    with open(file_path, "r") as file:
        json_data = json.load(file)

    while True: 
        idx = random.randint(0, len(json_data) - 1)
        entry = json_data[idx]
        words = ["悬疑", "推理", "侦探", "犯罪", "crime", "mystery", "detective"]
        if is_movie: 
            sentence = entry.get("subject").get("genres")
        else: 
            tags = entry.get("subject").get("tags")
            tags = "".join(tags) if tags is not None else ""
            sentence = tags + entry.get("subject").get("intro") 
        if check_word_in_sentence(words, sentence): 
            break 


    idx = entry.get("id")

    img_url = entry.get("subject").get("pic").get("large")

    rate = entry.get("subject").get("rating").get("value")
    rate = None if int(rate) == 0 else "{:.1f}".format(rate)

    review = entry.get("comment")
    review = None if len(review) == 0 else review
    if review is not None:
        if len(review) > 50:
            # too long
            review = None
        else:
            review = textwrap.wrap(review, width=20)
            review = "\n\n".join(review)
            review = "短评 | " + review

    genres = entry.get("subject").get("genres")

    date = entry.get("subject").get("pubdate")
    date = date[0] if isinstance(date, list) else date 

    author = entry.get("subject").get("author")
    author = author[0] if isinstance(author, list) else author

    if is_movie:
        date = "上映 | " + format_date(date)
        category = "类型 | " + " / ".join(genres)
    else:
        date = "出版 | " + format_date(date)
        category = "作者 | " + author 

    def convert_color(color):
        return tuple([int(c * 255) for c in color])

    base_color = entry.get("subject").get("color_scheme").get("_base_color")
    avg_color = entry.get("subject").get("color_scheme").get("_avg_color")
    color = [convert_color(base_color), convert_color(avg_color)]

    doubaninfo = DoubanInfo(
        idx,
        img_url,
        entry.get("subject").get("title"),
        rate,
        review,
        category,
        date,
        my_type == "movie",
        color,
    )

    return doubaninfo
