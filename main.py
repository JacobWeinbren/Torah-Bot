import random
from sefaria_api import get_sefaria_data
from text_processing import extract_text_from_data, split_content
from html_generator import generate_html_content
from screenshot_capture import capture_screenshot
from utils import save_image


def process_input(input_text):
    return " ".join(
        word for word in input_text.split() if not word.startswith("@")
    ).title()


def generate_image(ref, paired_lines, color1, color2, i):
    html_content = generate_html_content(ref, paired_lines, color1, color2)
    screenshot = capture_screenshot(html_content)
    filename = f"output_image_{i}.png"
    save_image(screenshot, filename)
    return filename, "\n".join(f"{ref}\n{h}\n{e}" for h, e in paired_lines)


def main(input_text):
    processed_text = process_input(input_text)
    data = get_sefaria_data({"title": "", "body": processed_text})
    reference, full_hebrew_text, full_english_text = extract_text_from_data(data)
    segments = split_content(reference, full_hebrew_text, full_english_text)

    colors = [
        "red",
        "orange",
        "amber",
        "yellow",
        "lime",
        "green",
        "emerald",
        "teal",
        "cyan",
        "sky",
        "blue",
        "indigo",
        "violet",
        "purple",
        "fuchsia",
        "pink",
        "rose",
    ]
    color1, color2 = random.sample(colors, 2)

    images, alt_texts = zip(
        *[
            generate_image(ref, paired_lines, color1, color2, i)
            for i, (ref, paired_lines) in enumerate(segments, 1)
        ]
    )

    return list(images), list(alt_texts), reference
