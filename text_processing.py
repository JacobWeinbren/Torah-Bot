from html import unescape
from hebrew import Hebrew
from itertools import zip_longest


def remove_cantillation(text):
    return Hebrew(text).no_taamim()


def extract_text_from_data(data):
    result = data["body"]["results"][0]
    if not result:
        raise ValueError("No references found in the body text.")

    ref = result["refs"][0]
    ref_data = data["body"]["refData"].get(ref, {})

    hebrew_texts = [
        str(remove_cantillation(unescape(text))) for text in ref_data.get("he", ["N/A"])
    ]
    english_texts = [unescape(text) for text in ref_data.get("en", ["N/A"])]

    return ref, "\n".join(hebrew_texts), "\n".join(english_texts)


def split_content(reference, hebrew_text, english_text, max_chars=1000, max_segments=4):
    hebrew_lines = hebrew_text.split("\n")
    english_lines = english_text.split("\n")

    segments = []
    current_segment = []
    current_length = len(reference)

    for h, e in zip_longest(hebrew_lines, english_lines, fillvalue=""):
        line_length = len(h) + len(e) + 3  # +3 for newline and space
        if current_length + line_length > max_chars and current_segment:
            segments.append((reference, current_segment))
            current_segment = []
            current_length = len(reference)

        current_segment.append((h, e))
        current_length += line_length

    if current_segment:
        segments.append((reference, current_segment))

    if len(segments) > max_segments:
        raise ValueError(
            f"The requested passage is too long. It requires {len(segments)} segments, but only {max_segments} are allowed."
        )

    if any(
        len(ref) + sum(len(h) + len(e) + 1 for h, e in seg) > max_chars
        for ref, seg in segments
    ):
        raise ValueError("One or more segments exceed the maximum character limit.")

    return segments
