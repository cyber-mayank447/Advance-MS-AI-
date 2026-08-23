from engine.automation import (
    type_text, press_key, hotkey, click, move_mouse, screenshot,
    open_folder, create_folder, list_folder, move_file, copy_file, delete_file
)

def handle_automation_command(query, speak):
    q = str(query).lower().strip()

    if q == "type hello":
        speak("Typing now, Mayank Sir.")
        return type_text("Hello Mayank Sir!")

    if q in ("press enter", "press escape", "press esc", "press tab", "press space"):
        key = {"press enter":"enter","press escape":"esc","press esc":"esc",
               "press tab":"tab","press space":"space"}[q]
        speak(f"Pressing {key}.")
        return press_key(key)

    if q in ("copy", "copy that"):
        speak("Copying, Mayank Sir.")
        return hotkey("ctrl","c")

    if q in ("paste", "paste that"):
        speak("Pasting, Mayank Sir.")
        return hotkey("ctrl","v")

    if q in ("select all", "select everything"):
        speak("Selecting all.")
        return hotkey("ctrl","a")

    if q in ("save", "save file"):
        speak("Saving.")
        return hotkey("ctrl","s")

    if q in ("take screenshot", "capture screen", "screenshot"):
        path = screenshot()
        speak("Screenshot le liya Mayank Sir.")
        return path

    if q in ("open downloads", "open download folder"):
        p = __import__("os").path.join(__import__("os").path.expanduser("~"), "Downloads")
        speak("Downloads folder khol rahi hoon.")
        return open_folder(p)

    if q in ("open desktop", "open desktop folder"):
        p = __import__("os").path.join(__import__("os").path.expanduser("~"), "Desktop")
        speak("Desktop khol rahi hoon.")
        return open_folder(p)

    if q.startswith("create folder "):
        name = query[len("create folder "):].strip()
        if not name:
            return False
        p = __import__("os").path.join(__import__("os").path.expanduser("~"), "Desktop", name)
        speak(f"Desktop par {name} folder bana rahi hoon.")
        return create_folder(p)

    if q.startswith("open folder "):
        name = query[len("open folder "):].strip()
        p = __import__("os").path.join(__import__("os").path.expanduser("~"), "Desktop", name)
        if __import__("os").path.isdir(p):
            speak(f"{name} folder khol rahi hoon.")
            return open_folder(p)
        speak("Mayank Sir, woh folder nahi mila.")
        return False

    if q in ("list desktop files", "show desktop files"):
        p = __import__("os").path.join(__import__("os").path.expanduser("~"), "Desktop")
        items = list_folder(p)
        speak(f"Desktop par {len(items)} items hain, Mayank Sir.")
        return True

    # File deletion is intentionally confirmation-gated.
    if q.startswith("delete file "):
        name = query[len("delete file "):].strip()
        speak(f"{name} delete karne ke liye bolo 'confirm delete {name}'.")
        return "WAIT_DELETE:" + name

    if q.startswith("confirm delete "):
        name = query[len("confirm delete "):].strip()
        p = __import__("os").path.join(__import__("os").path.expanduser("~"), "Desktop", name)
        if __import__("os").path.isfile(p):
            speak(f"Deleting {name}, Mayank Sir.")
            return delete_file(p)
        speak("Mayank Sir, Desktop par woh file nahi mili.")
        return False

    return None
