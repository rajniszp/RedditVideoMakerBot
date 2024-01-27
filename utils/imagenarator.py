import os
import re
from textwrap import wrap as wrap_text

from PIL import Image, ImageDraw, ImageFont
from rich.progress import track

from TTS.engine_wrapper import process_text

def getsize(font, text):
    (left, top, right, bottom) = font.getbbox(text)
    return right - left, bottom - top

def draw_multiple_line_text(
    image: Image, text: str, font: ImageFont.FreeTypeFont, text_color: tuple, padding: int, wrap=50, transparent=False
) -> None:
    """
    Draw multiline text over given image
    """
    draw = ImageDraw.Draw(image)
    ascent, descent = font.getmetrics()
    font_height = ascent + descent
    image_width, image_height = image.size
    lines = wrap_text(text, width=wrap)
    y = round(
        (image_height / 2) - (
        ((font_height + round(padding)) * len(lines)) / 2
    ))
    for line in lines:
        line_width, line_height = getsize(font, line)
        
        if transparent:
            shadowcolor = "black"
            for i in range(1, 5):
                draw.text(
                    ((image_width - line_width) / 2 - i, y - i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 + i, y - i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 - i, y + i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 + i, y + i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
        draw.text(((image_width - line_width) / 2, y), line, font=font, fill=text_color)
        y += font_height + padding


def imagemaker(theme: tuple, reddit_obj: dict, txtclr: tuple, padding=3, transparent=False, image_size: tuple = (1920,1080), font_size=100) -> None:
    """
    Render Images for video
    """
    title = process_text(reddit_obj["thread_title"], False)
    texts = reddit_obj["thread_post"]
    id = re.sub(r"[^\w\s-]", "", reddit_obj["thread_id"])

    if transparent:
        tfont = ImageFont.truetype(os.path.join("fonts", "Roboto-Black.ttf"), font_size)
        font = ImageFont.truetype(os.path.join("fonts", "Roboto-Bold.ttf"), font_size)
    else:
        tfont = ImageFont.truetype(
            os.path.join("fonts", "Roboto-Bold.ttf"), font_size
        )  # for title
        font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), font_size)

    image = Image.new("RGBA", image_size, theme)

    # for title
    draw_multiple_line_text(
        image, title, tfont, txtclr, padding, wrap=30, transparent=transparent
    )

    image.save(f"assets/temp/{id}/png/title.png")

    for idx, text in track(enumerate(texts), "Rendering Image"):
        image = Image.new("RGBA", image_size, theme)
        text = process_text(text, False)
        draw_multiple_line_text(
            image, text, font, txtclr, padding, wrap=30, transparent=transparent
        )
        image.save(f"assets/temp/{id}/png/img{idx}.png")
