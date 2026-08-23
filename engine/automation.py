import os
import subprocess
import time
import pyautogui

def type_text(text, interval=0.02):
    pyautogui.write(str(text), interval=interval)
    return True

def press_key(key):
    pyautogui.press(str(key))
    return True

def hotkey(*keys):
    pyautogui.hotkey(*[str(k) for k in keys])
    return True

def click(x=None, y=None):
    if x is None or y is None:
        pyautogui.click()
    else:
        pyautogui.click(int(x), int(y))
    return True

def move_mouse(x, y, duration=0.2):
    pyautogui.moveTo(int(x), int(y), duration=float(duration))
    return True

def screenshot(path="ms_screenshot.png"):
    path = os.path.abspath(path)
    pyautogui.screenshot(path)
    return path

def open_folder(path):
    path = os.path.abspath(os.path.expanduser(str(path)))
    if not os.path.exists(path):
        return False
    subprocess.Popen(["explorer", path])
    return True

def create_folder(path):
    path = os.path.abspath(os.path.expanduser(str(path)))
    os.makedirs(path, exist_ok=True)
    return True

def list_folder(path="."):
    path = os.path.abspath(os.path.expanduser(str(path)))
    return os.listdir(path) if os.path.isdir(path) else []

def move_file(source, destination):
    import shutil
    source = os.path.abspath(os.path.expanduser(str(source)))
    destination = os.path.abspath(os.path.expanduser(str(destination)))
    if not os.path.exists(source):
        return False
    shutil.move(source, destination)
    return True

def copy_file(source, destination):
    import shutil
    source = os.path.abspath(os.path.expanduser(str(source)))
    destination = os.path.abspath(os.path.expanduser(str(destination)))
    if not os.path.exists(source):
        return False
    shutil.copy2(source, destination)
    return True

def delete_file(path):
    import os
    path = os.path.abspath(os.path.expanduser(str(path)))
    if not os.path.isfile(path):
        return False
    os.remove(path)
    return True
