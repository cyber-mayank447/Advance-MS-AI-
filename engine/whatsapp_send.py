import time
import urllib.parse
import webbrowser
import pyautogui

def normalize_phone(phone):
    return "".join(ch for ch in str(phone) if ch.isdigit())

def open_chat(phone, message=""):
    digits = normalize_phone(phone)
    if not digits:
        return False
    text = urllib.parse.quote(str(message))
    webbrowser.open(f"https://web.whatsapp.com/send?phone={digits}&text={text}")
    return True

def send_message(phone, message, wait_seconds=8):
    """Open WhatsApp Web with prefilled text, then press Enter to send.

    The user must already be logged into WhatsApp Web. The wait gives the
    browser/chat time to load before the final Enter key is sent.
    """
    if not open_chat(phone, message):
        return False
    time.sleep(wait_seconds)
    pyautogui.press("enter")
    return True
