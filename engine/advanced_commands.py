import os, re
from engine.pc_control import open_app, close_app
from engine.pc_advanced import mouse_move, mouse_click, type_text, press_key, screenshot, create_folder, create_file, copy_path, move_path, delete_path
from engine.browser_control import new_tab, close_tab, back, forward, refresh, browser_search, open_url
from engine.voice_notes import record_voice
from engine.safety import request


def handle(query, speak):
    q=str(query).strip(); low=q.lower()
    # Browser
    if low in ('new tab','new tab kholo','naya tab kholo'):
        speak('New tab khol rahi hoon Mayank Sir.'); return new_tab()
    if low in ('close tab','ye tab band karo','tab band karo'):
        speak('Current tab band kar rahi hoon.'); return close_tab()
    if low in ('back','browser back','piche jao','peeche jao'):
        return back()
    if low in ('forward','browser forward','aage jao'):
        return forward()
    if low in ('refresh','refresh page','page refresh karo'):
        return refresh()
    m=re.match(r'^(?:google|google par)\s+(?:search|search karo|search for)\s+(.+)$',q,re.I) or re.match(r'^google search (.+)$',q,re.I)
    if m:
        return browser_search(m.group(1),'google')
    m=re.match(r'^(?:youtube|youtube par)\s+(?:search|search karo|search for)\s+(.+)$',q,re.I) or re.match(r'^youtube search (.+)$',q,re.I)
    if m: return browser_search(m.group(1),'youtube')
    # Screenshot
    if low in ('screenshot','take screenshot','screenshot le lo','screen shot'):
        path=screenshot(); speak(f'Screenshot save kar diya Mayank Sir: {path}'); return True
    # Mouse/keyboard
    m=re.match(r'^(?:move mouse|mouse move)\s+(\d+)\s+(\d+)$',q,re.I)
    if m: return mouse_move(int(m.group(1)),int(m.group(2)))
    m=re.match(r'^(?:click mouse|mouse click)(?:\s+(left|right))?$',q,re.I)
    if m: return mouse_click(m.group(1) or 'left')
    m=re.match(r'^(?:type|type this|likho)\s+(.+)$',q,re.I)
    if m: return type_text(m.group(1))
    # File operations
    m=re.match(r'^create folder\s+(.+)$',q,re.I)
    if m: create_folder(m.group(1)); speak('Folder create ho gaya Mayank Sir.'); return True
    m=re.match(r'^create file\s+(.+)$',q,re.I)
    if m: create_file(m.group(1)); speak('File create ho gayi Mayank Sir.'); return True
    m=re.match(r'^copy\s+(.+?)\s+to\s+(.+)$',q,re.I)
    if m: copy_path(m.group(1),m.group(2)); speak('Copy complete Mayank Sir.'); return True
    m=re.match(r'^move\s+(.+?)\s+to\s+(.+)$',q,re.I)
    if m: move_path(m.group(1),m.group(2)); speak('Move complete Mayank Sir.'); return True
    m=re.match(r'^delete\s+(.+)$',q,re.I)
    if m:
        request('delete', {'path':m.group(1).strip()}); speak(f'{m.group(1).strip()} permanently delete karna hai. Confirm bolo.'); return 'WAIT_CONFIRM'
    # Voice note recording
    m=re.match(r'^(?:record|voice note record karo|voice message record karo)(?:\s+(\d+))?$',q,re.I)
    if m:
        seconds=int(m.group(1) or 10); speak(f'{seconds} second ki voice note recording start.'); path=record_voice(seconds); speak(f'Voice note save ho gayi: {path}'); return True
    return None
