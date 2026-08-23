import os
import webbrowser
from pathlib import Path

from engine.browser_control import open_url


def _open_folder(path):
    path = str(Path(path).expanduser())
    if os.name == 'nt':
        os.startfile(path)
    else:
        import subprocess
        subprocess.Popen(['xdg-open', path])
    return True


def run_macro(name, speak):
    n = name.strip().lower()
    home = Path.home()
    desktop = home / 'Desktop'
    if n in ('study mode', 'study mode start', 'start study mode'):
        webbrowser.open('https://www.google.com')
        webbrowser.open('https://www.youtube.com')
        _open_folder(desktop)
        speak('Study mode start kar diya Mayank Sir — Google, YouTube aur Desktop ready hain.')
        return True
    if n in ('work mode', 'start work mode'):
        webbrowser.open('https://mail.google.com')
        _open_folder(home / 'Documents')
        speak('Work mode ready hai Mayank Sir.')
        return True
    if n in ('desktop mode', 'open desktop'):
        _open_folder(desktop)
        speak('Desktop khol diya Mayank Sir.')
        return True
    return None
