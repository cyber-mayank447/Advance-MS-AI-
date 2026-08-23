import urllib.parse
import webbrowser
import pyautogui


def open_url(url):
    webbrowser.open(url); return True


def new_tab():
    pyautogui.hotkey('ctrl', 'l'); pyautogui.hotkey('ctrl', 'enter') if False else None
    pyautogui.hotkey('ctrl', 't'); return True


def close_tab(): pyautogui.hotkey('ctrl', 'w'); return True

def back(): pyautogui.hotkey('alt', 'left'); return True

def forward(): pyautogui.hotkey('alt', 'right'); return True

def refresh(): pyautogui.hotkey('ctrl', 'r'); return True

def focus_address(): pyautogui.hotkey('ctrl', 'l'); return True

def browser_search(query, engine='google'):
    q = urllib.parse.quote_plus(str(query).strip())
    if engine == 'youtube': url = f'https://www.youtube.com/results?search_query={q}'
    else: url = f'https://www.google.com/search?q={q}'
    return open_url(url)
