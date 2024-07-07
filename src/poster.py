from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

import image
import utils


class Poster:

    def __init__(self, background, poster, font, rate):
        self.background = background
        self.poster = poster.resize((450, 684))
        self.font = font
        self.rate = rate

        self.create_poster()

    def create_poster(self):
        self.background.paste(self.poster, (0, 0))

        if self.rate is not None:
            draw = ImageDraw.Draw(self.background)
            image.write_text(
                draw,
                "black",
                (790, 70),
                "Score: " + str(self.rate),
                self.font,
                40,
            )
