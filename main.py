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
    hebrew_texts = []
    english_texts = []

    try:
        data = get_sefaria_data(text)
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

        for i, (ref, paired_lines) in enumerate(segments, 1):
            html_content = generate_html_content(ref, paired_lines, color1, color2)
            screenshot = capture_screenshot(html_content)
            filename = f"output_image_{i}.png"
            save_image(screenshot, filename)
            images.append(filename)
            
            segment_hebrew = "\n".join([pair[0] for pair in paired_lines])
            segment_english = "\n".join([pair[1] for pair in paired_lines])
            hebrew_texts.append(segment_hebrew)
            english_texts.append(segment_english)
            alt_texts.append(f"{ref}\n{segment_hebrew}\n{segment_english}")

        image_count = len(segments)
        print(f"Generated {'image' if image_count == 1 else 'images'}: {image_count}")
        return images, alt_texts, reference, hebrew_texts, english_texts
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [], [], "", [], []

