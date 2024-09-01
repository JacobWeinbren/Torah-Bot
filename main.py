import random
from sefaria_api import get_sefaria_data
from text_processing import extract_text_from_data, split_content
from html_generator import generate_html_content
from screenshot_capture import capture_screenshot
from utils import save_image
import re
import random
from titlecase import titlecase
from colour import Color


def process_input(input_text):
    # Remove words starting with '@' and join the remaining words
    filtered_text = " ".join(
        word for word in input_text.split() if not word.startswith("@")
    )
    # Apply proper title case
    return titlecase(filtered_text)


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
    # Generate a random hue
    hue = random.random()

    # Create two colors with the random hue, offset by 0.5 (complementary)
    color1 = Color(hsl=(hue, 0.6, 0.85))
    color2 = Color(hsl=((hue + 0.2) % 1, 0.6, 0.85))

    # Convert to hex
    hex1 = color1.hex_l
    hex2 = color2.hex_l

    return hex1, hex2


def main(input_text):
    try:
        processed_text = process_input(input_text)
        data = get_sefaria_data(processed_text)
        reference, hebrew_text, english_text = extract_text_from_data(data)
        segments = split_content(reference, hebrew_text, english_text)

        images = []
        alt_texts = []
        color1, color2 = generate_vibrant_colors()

        for i, (ref, paired_lines) in enumerate(segments):
            image, alt_text = generate_image(ref, paired_lines, color1, color2, i)
            images.append(image)
            alt_texts.append(alt_text)

        return images, alt_texts, reference
    except ValueError as e:
        return None, None, str(e)
    except Exception as e:
        print(f"Error type: {type(e).__name__}", e)
        return (
            None,
            None,
            "An unexpected error occurred.",
        )
