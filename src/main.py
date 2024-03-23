import pathlib
from PIL import Image
from PIL import ImageDraw
import image
import os
import argparse

import utils
import get_info
import data

# Get the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()


def main(url, img_url, review, imdb_score=None, tomato_score=None, delete_images=False):
    # Create folder to save the poster image
    utils.create_folder()

    # Generate a unique filename for the poster image
    output_dir = current_dictionary / "../images"
    if delete_images:
        utils.delete_files_in_directory(output_dir)

    download_image_from_douban = True if img_url is None else False 
    doubaninfo = get_info.get_info_from_url(url, download_image_from_douban)

    path = current_dictionary / "../assets/bgimage.png"
    if not download_image_from_douban:
        utils.save_image_from_url(img_url, path)

    id = 0
    name = doubaninfo.title
    tag = ""
    year = doubaninfo.date
    category = doubaninfo.category

    # Get the lyrics of the song
    color = (50, 47, 48)
    if review is not None:
        music_lyrics = "短评 | " + review

    # Open the banner image
    banner = Image.open(path)
    default_size = 1000 
    width, height = banner.size
    if min(width, height) < default_size: 
        banner = utils.resize_image(banner)
    else:
        size = (default_size, default_size)
        banner.thumbnail(size, Image.Resampling.LANCZOS)

    # Open the poster template image
    poster = utils.create_image(1140, 1740)

    # Specify the region where you want to paste 'banner' onto 'background'
    left = 260
    top = 60
    utils.draw_on_poster(top, left, poster, banner)

    font_regular = f"../fonts/cn/wenyi.ttf"
    font_bold = f"../fonts/cn/wenyi.ttf"
    font_light = f"../fonts/cn/wenyi.ttf"

    # Create ImageDraw object for drawing on the poster
    draw = ImageDraw.Draw(poster)

    # Draw the color palette on the poster
    color_palette = image.draw_palette(draw, path, True)

    image.write_text(draw, color_palette[2], (60, 1204), name, font_bold, 50)

    image.write_text(draw, color_palette[2], (60, 1298), year, font_regular, 40)

    image.write_text(draw, color_palette[2], (60, 1350), category, font_regular, 40)

    if review is not None:
        image.write_multiline_text(
            draw, color_palette[2], (60, 1400), music_lyrics, font_light, 40
        )

    if doubaninfo.rate is not None:
        svg_image = utils.create_badge("green", "douban", str(doubaninfo.rate))
        # output_path = os.path.join(output_dir, "douban.png")
        # svg_image.save(output_path)
        left = 50
        top = 1120
        utils.draw_on_poster(top, left, poster, svg_image)

    if doubaninfo.is_movie and imdb_score is not None:
        svg_image = utils.create_badge("yellow", "imdb", str(imdb_score))
        # output_path = os.path.join(output_dir, "imdb.png")
        # svg_image.save(output_path)
        left = left + 300
        top = 1120
        utils.draw_on_poster(top, left, poster, svg_image)

    if doubaninfo.is_movie and tomato_score is not None:
        svg_image = utils.create_badge("red", "Rotten Tomato", str(tomato_score))
        # output_path = os.path.join(output_dir, "imdb.png")
        # svg_image.save(output_path)
        left = left + 300
        top = 1120
        utils.draw_on_poster(top, left, poster, svg_image)

    path = current_dictionary / "../assets/logo.png"
    with Image.open(path) as banner:
        size = (200, 200)
        banner.thumbnail(size, Image.Resampling.LANCZOS)
    left = 900
    top = 1500
    utils.draw_on_poster(top, left, poster, banner)

    formatted_date = utils.print_date_cn()
    image.write_text(draw, color_palette[5], (20, 1600), formatted_date, font_bold, 80)

    filename = f"{utils.create_filename(name, year)}_{utils.special_code()}"
    output_path = os.path.join(output_dir, f"{filename}.png")

    # Save the poster image
    poster.save(output_path, quality=100)
    print(f"[☕] Image saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data from database.")
    parser.add_argument("--random", action="store_true", help="Load a random entry")
    parser.add_argument("--delete", action="store_true", help="Delete the images")
    args = parser.parse_args()

    entry = data.load_one_entry(args.random)

    main(
        entry.get("web_url"),
        entry.get("image_url"),
        entry.get('review'),
        entry.get("imdb_score"),
        entry.get("tomato_score"),
        args.delete, 
    )
