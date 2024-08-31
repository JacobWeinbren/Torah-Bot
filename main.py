from sefaria_api import get_sefaria_data
from text_processing import extract_text_from_data, split_content
from html_generator import generate_html_content
from screenshot_capture import capture_screenshot
from utils import save_image


def process_input(input_text):
    # Remove username (assuming it's at the beginning and followed by a space)
    text_without_username = " ".join(input_text.split()[1:])
    return text_without_username.title()


def main(input_text):
    processed_text = process_input(input_text)
    text = {
        "title": "",
        "body": processed_text,
    }

    images = []
    alt_texts = []

    try:
        data = get_sefaria_data(text)
        reference, hebrew_text, english_text = extract_text_from_data(data)
        segments = split_content(reference, hebrew_text, english_text)

        for i, (ref, paired_lines) in enumerate(segments, 1):
            html_content = generate_html_content(ref, paired_lines)
            screenshot = capture_screenshot(html_content)
            filename = f"output_image_{i}.png"
            save_image(screenshot, filename)
            images.append(filename)
            alt_texts.append(f"Image {i} of {len(segments)}: {ref}")

        print(f"Generated {len(segments)} image(s).")
        return images, alt_texts
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [], []


if __name__ == "__main__":
    sample_input = (
        "@bot this contains complex text. something like this: shemot 14:19-30"
    )
    main(sample_input)
