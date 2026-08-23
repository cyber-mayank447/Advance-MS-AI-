import os, time
from pathlib import Path

from engine.pc_advanced import screenshot

try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None


def capture_and_read():
    path = screenshot()
    text = ''
    if pytesseract and Image:
        try:
            text = pytesseract.image_to_string(Image.open(path)).strip()
        except Exception as exc:
            text = f'OCR unavailable: {exc}'
    return path, text


def describe_screen(speak):
    path, text = capture_and_read()
    if text and not text.startswith('OCR unavailable'):
        preview = ' '.join(text.split())[:700]
        speak(f'Screen ka readable text mil gaya: {preview}')
    else:
        speak(f'Screenshot le liya Mayank Sir: {path}. Screen text reading ke liye Tesseract install hona chahiye.')
    return path
