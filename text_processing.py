from html import unescape
from hebrew import Hebrew


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

    hebrew_texts = [str(remove_cantillation(unescape(text))) for text in hebrew_texts]
    english_texts = [unescape(text) for text in english_texts]

    hebrew_text = "\n".join(hebrew_texts)
    english_text = "\n".join(english_texts)

    return ref, hebrew_text, english_text


def split_content(reference, hebrew_text, english_text, max_chars=1000):
    hebrew_lines = hebrew_text.split("\n")
    english_lines = english_text.split("\n")
    paired_lines = list(zip(hebrew_lines, english_lines))

    segments = []
    current_segment = []
    current_length = len(reference)

    for h, e in paired_lines:
        line_length = len(reference) + 2 + len(h) + 1 + len(e)
        if current_length + line_length > max_chars and current_segment:
            segments.append((reference, current_segment))
            current_segment = []
            current_length = len(reference)

        current_segment.append((h, e))
        current_length += len(h) + 1 + len(e)

    if current_segment:
        segments.append((reference, current_segment))

    return segments[:4]
