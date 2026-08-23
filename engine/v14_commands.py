import re
import webbrowser
from pathlib import Path

from engine.browser_control import new_tab, close_tab, back, forward, refresh, browser_search
from engine.pc_advanced import mouse_move, mouse_click, type_text, press_key
from engine.safety import request
from engine.v14_screen import describe_screen
from engine.v14_macros import run_macro


def _app_alias(name):
    n = name.lower().strip()
    aliases = {
        'notepad': 'notepad.exe', 'calculator': 'calc.exe', 'calc': 'calc.exe',
        'paint': 'mspaint.exe', 'explorer': 'explorer.exe', 'file explorer': 'explorer.exe',
    }
    return aliases.get(n)


def _open_app(name):
    import subprocess
    exe = _app_alias(name)
    if not exe:
        return None
    subprocess.Popen(exe, shell=True)
    return True


def handle_v14_command(query, speak):
    q = str(query).strip()
    low = q.lower()

    # Browser controls
    if low in ('new tab', 'new tab kholo', 'naya tab kholo'):
        speak('New tab khol rahi hoon Mayank Sir.'); return new_tab()
    if low in ('close tab', 'ye tab band karo', 'tab band karo'):
        speak('Tab close kar rahi hoon.'); return close_tab()
    if low in ('browser back', 'back karo', 'pichla page', 'back'):
        return back()
    if low in ('browser forward', 'forward karo', 'aage jao', 'forward'):
        return forward()
    if low in ('refresh', 'page refresh karo', 'refresh page'):
        return refresh()
    if low.startswith('google par ') or low.startswith('google pe '):
        term = re.sub(r'^google (par|pe)\s+', '', q, flags=re.I).strip()
        speak(f'Google par {term} search kar rahi hoon.'); return browser_search(term, 'google')
    if low.startswith('youtube par ') or low.startswith('youtube pe '):
        term = re.sub(r'^youtube (par|pe)\s+', '', q, flags=re.I).strip()
        speak(f'YouTube par {term} search kar rahi hoon.'); return browser_search(term, 'youtube')
    if low.startswith('youtube kholo'):
        webbrowser.open('https://youtube.com'); return True
    if low in ('chrome kholo', 'chrome open karo', 'google chrome kholo'):
        webbrowser.open('https://www.google.com'); speak('Chrome ready hai Mayank Sir.'); return True

    # PC apps
    m = re.match(r'^(?:open|start|khol(?:o)?|chala(?:o)?)\s+(notepad|calculator|calc|paint|file explorer|explorer)$', low)
    if m:
        speak(f'{m.group(1)} khol rahi hoon Mayank Sir.'); return _open_app(m.group(1))

    # Mouse / keyboard
    m = re.match(r'^(?:mouse|cursor)\s+(?:move|le jao)\s+(\d+)\s+(\d+)$', low)
    if m:
        mouse_move(m.group(1), m.group(2)); speak('Mouse move kar diya.'); return True
    m = re.match(r'^(?:click|click karo)\s+(\d+)\s+(\d+)$', low)
    if m:
        mouse_move(m.group(1), m.group(2)); mouse_click(); speak('Click kar diya Mayank Sir.'); return True
    m = re.match(r'^(?:type|likho)\s+(.+)$', q, re.I)
    if m:
        type_text(m.group(1)); return True
    m = re.match(r'^press\s+([a-z0-9_]+)$', low)
    if m:
        press_key(m.group(1)); return True

    # Screen OCR
    if low in ('screen read karo', 'screen par kya hai', 'screen dekho', 'screen analyze karo', 'screen analyse karo'):
        return describe_screen(speak)

    # Macros
    if low in ('study mode', 'study mode start', 'start study mode', 'work mode', 'start work mode', 'desktop mode'):
        return run_macro(low, speak)

    # Safer file operations with explicit paths
    m = re.match(r'^create folder (.+)$', q, re.I)
    if m:
        p = Path(m.group(1).strip()).expanduser()
        p.mkdir(parents=True, exist_ok=True); speak(f'Folder bana diya: {p}'); return True

    m = re.match(r'^delete (.+)$', q, re.I)
    if m:
        p = Path(m.group(1).strip()).expanduser()
        if not p.exists(): speak('Ye file ya folder nahi mila.'); return False
        request('delete', {'path': str(p)})
        speak(f'{p} permanently delete karna hai. Confirm bolo.'); return 'WAIT_CONFIRM'

    return None
