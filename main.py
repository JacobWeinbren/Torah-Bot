import random
from sefaria_api import get_sefaria_data
from text_processing import extract_text_from_data, split_content
from html_generator import generate_html_content
from screenshot_capture import capture_screenshot
from utils import save_image
import re
import random
import colorsys


def process_input(input_text):
    return " ".join(
        word for word in input_text.split() if not word.startswith("@")
    ).title()


def remove_html_tags(text):
    return re.sub("<[^<]+?>", "", text)


def generate_image(ref, paired_lines, color1, color2, i):
    html_content = generate_html_content(ref, paired_lines, color1, color2)
    screenshot = capture_screenshot(html_content)
    filename = f"output_image_{i}.png"
    save_image(screenshot, filename)
    return filename, f"{ref}\n" + "\n".join(
        f"{remove_html_tags(h)}\n{remove_html_tags(e)}" for h, e in paired_lines
    )


def generate_vibrant_colors():
    hue = random.random()
    saturation = 0.5
    lightness = 0.9

    rgb1 = colorsys.hls_to_rgb(hue, lightness, saturation)
    rgb2 = colorsys.hls_to_rgb((hue + 0.33) % 1, lightness, saturation)

    hex1 = "#{:02x}{:02x}{:02x}".format(
        int(rgb1[0] * 255), int(rgb1[1] * 255), int(rgb1[2] * 255)
    )
    hex2 = "#{:02x}{:02x}{:02x}".format(
        int(rgb2[0] * 255), int(rgb2[1] * 255), int(rgb2[2] * 255)
    )

    return hex1, hex2


def main(input_text):
    processed_text = process_input(input_text)
    data = get_sefaria_data({"title": "", "body": processed_text})
    reference, full_hebrew_text, full_english_text = extract_text_from_data(data)
    segments = split_content(reference, full_hebrew_text, full_english_text)

    color1, color2 = generate_vibrant_colors()

    images, alt_texts = zip(
        *[
            generate_image(ref, paired_lines, color1, color2, i)
            for i, (ref, paired_lines) in enumerate(segments, 1)
        ]
    )

    return list(images), list(alt_texts), reference
