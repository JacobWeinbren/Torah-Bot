import requests
import re
from playwright.sync_api import sync_playwright
from html import unescape
import random
from hebrew import Hebrew


def get_sefaria_data(text):
    url = "https://www.sefaria.org/api/find-refs?with_text=1"
    response = requests.post(url, json={"text": text})
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}\n{response.text}")
    return response.json()


def remove_cantillation(text):
    return Hebrew(text).no_taamim()


def extract_text_from_data(data):
    result = data["body"]["results"][0]
    if not result:
        raise Exception("No references found in the body text.")

    ref = result["refs"][0]
    ref_data = data["body"]["refData"].get(ref, {})
    hebrew_texts = ref_data.get("he", ["N/A"])
    english_texts = ref_data.get("en", ["N/A"])

    # Remove cantillation marks from Hebrew texts, convert to string, and unescape both
    hebrew_texts = [str(remove_cantillation(unescape(text))) for text in hebrew_texts]
    english_texts = [unescape(text) for text in english_texts]

    # Join the texts with line breaks
    hebrew_text = "\n".join(hebrew_texts)
    english_text = "\n".join(english_texts)

    return ref, hebrew_text, english_text


def generate_html_content(reference, hebrew_text, english_text):
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

    # Split the texts into lines
    hebrew_lines = hebrew_text.split("\n")
    english_lines = english_text.split("\n")

    # Create paired lines of Hebrew and English
    paired_lines = zip(hebrew_lines, english_lines)
    content = "\n".join(
        [
            f'<div class="mb-8">'
            f'<div class="text-right text-2xl sm:text-3xl md:text-4xl leading-relaxed text-gray-800 mb-2" dir="rtl">{h}</div>'
            f'<div class="text-left text-xl sm:text-2xl md:text-3xl leading-relaxed text-gray-700">{e}</div>'
            f"</div>"
            for h, e in paired_lines
        ]
    )

    return f"""
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Frank Ruhl Libre', serif; }}
        </style>
    </head>
    <body class="bg-gradient-to-br from-{color1}-100 to-{color2}-100 min-h-screen flex items-center justify-center p-4 sm:p-8 md:p-16">
        <div class="w-full max-w-4xl bg-white/80 backdrop-blur-sm rounded-xl shadow-2xl overflow-hidden">
            <div class="p-6 sm:p-10">
                <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold mb-6 text-center text-gray-800 border-b pb-4">{reference}</h1>
                <div class="space-y-8">
                    {content}
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def capture_screenshot(html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        page.wait_for_timeout(1000)

        # Get the bounding box of the content
        content_box = page.query_selector("body > div").bounding_box()

        # Set viewport and content size to ensure all content is visible
        page.set_viewport_size(
            {
                "width": int(content_box["width"]) + 120,
                "height": int(content_box["height"]) + 120,
            }
        )

        # Capture the screenshot of the entire page
        screenshot = page.screenshot(full_page=True)

        browser.close()
    return screenshot


def save_image(screenshot, filename="output_image.png"):
    with open(filename, "wb") as f:
        f.write(screenshot)
    print(f"Image generated: {filename}")
    print(f"Image size: {len(screenshot) / 1024:.2f} KB")


def main():
    text = {
        "title": "",
        "body": "this contains complex text. something like this: shemot 14:19-30".title(),
    }

    try:
        data = get_sefaria_data(text)
        reference, hebrew_text, english_text = extract_text_from_data(data)
        
        # Check the combined length of reference and context text
        context_text = f"{reference}\n{hebrew_text}\n{english_text}"
        if len(context_text) <= 1000:
            html_content = generate_html_content(reference, hebrew_text, english_text)
            screenshot = capture_screenshot(html_content)
            save_image(screenshot)
        else:
            print("Content exceeds 1000 characters. Image generation skipped.")
            print(f"Total characters: {len(context_text)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
