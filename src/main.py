import pathlib
from PIL import Image
from PIL import ImageDraw
import image
import os 

import utils 

# Get the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()

# Get the path of the image
path = current_dictionary / "../assets/test2.png"
id = 0
name = "test"
year = "2000"
artist = "tim"
duration = "1h"
label = "label"

# Get the lyrics of the song
color = (50, 47, 48)
music_lyrics = "a sample"

# Open the banner image
with Image.open(path) as banner:
    size = (510, 510)
    banner.thumbnail(size, Image.Resampling.LANCZOS)

# Open the poster template image
poster = utils.create_image(570, 870)

# Specify the region where you want to paste 'banner' onto 'background'
left = 110
top = 30
right = left + banner.width
bottom = top + banner.height
box = (left, top, right, bottom)

# Paste the banner image onto the poster
poster.paste(banner, box)

# Set font family and paths
FONT_FAMILY = "Oswald"

# font_dir = pathlib.Path.resolve(current_dictionary / f"../fonts/{FONT_FAMILY}/")

font_regular = f"../fonts/Oswald/{FONT_FAMILY}-Regular.ttf"
font_bold = f"../fonts/Oswald/{FONT_FAMILY}-Bold.ttf"
font_light = f"../fonts/Oswald/{FONT_FAMILY}-Light.ttf"

# Create ImageDraw object for drawing on the poster
draw = ImageDraw.Draw(poster)

# Draw the color palette on the poster
image.draw_palette(draw, path, True)

# Write the title (song name and year) on the poster
image.write_title(draw, (30, 602, 400, 637), name, year, font_bold, 40)

# Write the artist name and duration on the poster
image.write_text(draw, (30, 649), artist, font_regular, 30)
image.write_text(draw, (496, 617), duration, font_regular, 20)

# Write the lyrics on the poster
image.write_multiline_text(draw, (30, 685), music_lyrics, font_light, 21)

# Write the label information on the poster
# image.write_text(
#     draw,
#     (545, 810),
#     label[0],
#     str(font_regular),
#     13,
#     anchor="rt",
# )

# image.write_text(
#     draw,
#     (545, 825),
#     label[1],
#     str(font_regular),
#     13,
#     anchor="rt",
# )

# Create folder to save the poster image
utils.create_folder()

# Generate a unique filename for the poster image
output_dir = current_dictionary / "../images"
utils.delete_files_in_directory(output_dir)

filename = f"{utils.create_filename(name, artist)}_{utils.special_code()}"
output_path = os.path.join(output_dir, f"{filename}.png")

# Save the poster image
poster.save(output_path)
print(f"[☕] Image saved to {output_path}")
