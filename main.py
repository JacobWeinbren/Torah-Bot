from sefaria_api import get_sefaria_data
from text_processing import extract_text_from_data, split_content
from html_generator import generate_html_content
from screenshot_capture import capture_screenshot
from utils import save_image
import random


def process_input(input_text):
    # Remove words starting with '@'
    words = input_text.split()
    text_without_username = " ".join(word for word in words if not word.startswith("@"))
    return text_without_username.title()


def main(input_text):
    processed_text = process_input(input_text)
    text = {
        "title": "",
        "body": processed_text,
    }

    images = []
    alt_texts = []
    reference = ""

    try:
        data = get_sefaria_data(text)
        reference, hebrew_text, english_text = extract_text_from_data(data)
        segments = split_content(reference, hebrew_text, english_text)

        # Generate random colors once for all images
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

        for i, (ref, paired_lines) in enumerate(segments, 1):
            html_content = generate_html_content(ref, paired_lines, color1, color2)
            screenshot = capture_screenshot(html_content)
            filename = f"output_image_{i}.png"
            save_image(screenshot, filename)
            images.append(filename)
            alt_texts.append(f"Image {i} of {len(segments)}: {ref}")

        image_count = len(segments)
        print(f"Generated {'image' if image_count == 1 else 'images'}: {image_count}")
        return images, alt_texts, reference
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [], [], ""
