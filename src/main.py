import pathlib
from PIL import Image
from PIL import ImageDraw
import image
import os
import argparse

import utils
import data
import config 

# Get the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()


def main():
    doubaninfo = data.load_one_entry()
    
    # Create folder to save the poster image
    utils.create_folder()

    # Generate a unique filename for the poster image
    output_dir = current_dictionary / "../images"
    if config.delete_images:
        utils.delete_files_in_directory(output_dir)

    path = current_dictionary / "../assets/bgimage.png"
    successful = utils.save_image_from_url(doubaninfo.img_url, path)
    if not successful: 
       path = current_dictionary / "../assets/logo.png" 

    # Get the lyrics of the song
    color = (50, 47, 48)

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
    image.draw_palette(draw, path, doubaninfo.color[0])

    image.write_text(draw, doubaninfo.color[1], (60, 1204), doubaninfo.title, font_bold, 50)

    image.write_text(draw, doubaninfo.color[1], (60, 1298), doubaninfo.date, font_regular, 40)

    image.write_text(draw, doubaninfo.color[1], (60, 1350), doubaninfo.category, font_regular, 40)

    if doubaninfo.review is not None:
        image.write_multiline_text(
            draw, doubaninfo.color[1], (60, 1400), doubaninfo.review, font_light, 40
        )

    if doubaninfo.rate is not None:
        svg_image = utils.create_badge("green", "douban", str(doubaninfo.rate))
        # output_path = os.path.join(output_dir, "douban.png")
        # svg_image.save(output_path)
        left = 50
        top = 1120
        utils.draw_on_poster(top, left, poster, svg_image)

    if doubaninfo.is_movie and config.show_imdb:
        svg_image = utils.create_badge("yellow", "imdb", str(imdb_score))
        # output_path = os.path.join(output_dir, "imdb.png")
        # svg_image.save(output_path)
        left = left + 300
        top = 1120
        utils.draw_on_poster(top, left, poster, svg_image)

    if doubaninfo.is_movie and config.show_tomato:
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
    image.write_text(draw, doubaninfo.color[1], (20, 1600), formatted_date, font_bold, 80)

    filename = f"{utils.create_filename(doubaninfo.title, doubaninfo.date)}_{utils.special_code()}"
    utils.save_image_with_filename(poster, filename)
    filename = "daily"
    utils.save_image_with_filename(poster, filename)

if __name__ == "__main__":
    main()
