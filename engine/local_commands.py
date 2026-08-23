import ast
import datetime as dt
import os
import platform
import re
import subprocess
import webbrowser
from urllib.parse import quote_plus

from engine.command import speak


def _safe_calculate(expression: str):
    expression = expression.strip().replace('x', '*').replace('÷', '/')
    if len(expression) > 80 or not re.fullmatch(r'[0-9+\-*/().% ]+', expression):
        raise ValueError('unsupported expression')

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = eval_node(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)):
            left, right = eval_node(node.left), eval_node(node.right)
            if isinstance(node.op, ast.Add): return left + right
            if isinstance(node.op, ast.Sub): return left - right
            if isinstance(node.op, ast.Mult): return left * right
            if isinstance(node.op, ast.Div): return left / right
            return left % right
        raise ValueError('unsupported expression')

    tree = ast.parse(expression, mode='eval')
    result = eval_node(tree)
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return result


def handle_local_command(query: str) -> bool:
    q = query.lower().strip()

    if q in {'time', "what's the time", 'what is the time', 'current time'} or 'what time is it' in q:
        speak(f"Mayank Sir, the time is {dt.datetime.now().strftime('%I:%M %p')}")
        return True

    if q in {'date', 'today', "today's date", 'what is the date'} or 'what date is it' in q:
        speak(f"Mayank Sir, today is {dt.datetime.now().strftime('%A, %d %B %Y')}")
        return True

    if q.startswith('calculate ') or q.startswith('what is '):
        expression = re.sub(r'^(calculate|what is)\s+', '', q).strip()
        if re.fullmatch(r'[0-9+\-*/().% x÷ ]+', expression):
            try:
                speak(f"Mayank Sir, the answer is {_safe_calculate(expression)}")
            except Exception:
                speak("Mayank Sir, I couldn't calculate that.")
            return True

    if q in {'open google', 'google'}:
        webbrowser.open('https://www.google.com')
        speak('Opening Google, Mayank Sir.')
        return True
    if q in {'open youtube', 'youtube'}:
        webbrowser.open('https://www.youtube.com')
        speak('Opening YouTube, Mayank Sir.')
        return True
    if q in {'open github', 'github'}:
        webbrowser.open('https://github.com')
        speak('Opening GitHub, Mayank Sir.')
        return True
    if q in {'open whatsapp', 'whatsapp'}:
        os.system('start whatsapp:')
        speak('Opening WhatsApp, Mayank Sir.')
        return True

    if q.startswith(('search google for ', 'google search for ', 'search for ')):
        term = re.sub(r'^(search google for|google search for|search for)\s+', '', q).strip()
        if term:
            webbrowser.open('https://www.google.com/search?q=' + quote_plus(term))
            speak(f"Searching Google for {term}, Mayank Sir.")
        return True

    if q.startswith(('search youtube for ', 'youtube search for ')):
        term = re.sub(r'^(search youtube for|youtube search for)\s+', '', q).strip()
        if term:
            webbrowser.open('https://www.youtube.com/results?search_query=' + quote_plus(term))
            speak(f"Searching YouTube for {term}, Mayank Sir.")
        return True

    if q in {'volume up', 'increase volume', 'increase the volume'}:
        import pyautogui
        pyautogui.press('volumeup', presses=3, interval=0.05)
        speak('Volume increased, Mayank Sir.')
        return True
    if q in {'volume down', 'decrease volume', 'decrease the volume'}:
        import pyautogui
        pyautogui.press('volumedown', presses=3, interval=0.05)
        speak('Volume decreased, Mayank Sir.')
        return True
    if q in {'mute', 'mute volume', 'unmute'}:
        import pyautogui
        pyautogui.press('volumemute')
        speak('Volume toggled, Mayank Sir.')
        return True

    if q in {'lock pc', 'lock computer', 'lock my pc'}:
        subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=False)
        return True

    if q in {'system info', 'computer info', 'pc info'}:
        info = f"You are running {platform.system()} {platform.release()} on {platform.machine()}"
        speak(f"Mayank Sir, {info}.")
        return True

    return False
