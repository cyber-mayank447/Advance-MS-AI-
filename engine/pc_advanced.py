import os
import shutil
import subprocess
import time
from pathlib import Path

import pyautogui

SCREENSHOT_DIR = Path(os.path.expanduser('~/Pictures/MS_Screenshots'))


def mouse_move(x, y, duration=0.2):
    pyautogui.moveTo(int(x), int(y), duration=float(duration)); return True


def mouse_click(button='left', clicks=1):
    pyautogui.click(button=button, clicks=int(clicks)); return True


def type_text(text, interval=0.02):
    pyautogui.write(str(text), interval=float(interval)); return True


def press_key(key, presses=1):
    pyautogui.press(key, presses=int(presses), interval=0.05); return True


def screenshot(path=None):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if path:
        target = Path(path).expanduser()
    else:
        target = SCREENSHOT_DIR / time.strftime('MS_%Y%m%d_%H%M%S.png')
    target.parent.mkdir(parents=True, exist_ok=True)
    pyautogui.screenshot(str(target))
    return str(target)


def create_folder(path):
    Path(path).expanduser().mkdir(parents=True, exist_ok=True); return True


def create_file(path, content=''):
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(str(content), encoding='utf-8'); return True


def copy_path(src, dst):
    src, dst = Path(src).expanduser(), Path(dst).expanduser()
    if src.is_dir(): shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
    return True


def move_path(src, dst):
    src, dst = Path(src).expanduser(), Path(dst).expanduser()
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst)); return True


def delete_path(path):
    target = Path(path).expanduser()
    if target.is_dir(): shutil.rmtree(target)
    elif target.exists(): target.unlink()
    return True
