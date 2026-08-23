import os
import time
import webbrowser
import subprocess

def open_chrome(url=None):
    url = url or "https://www.google.com"
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    chrome = next((p for p in candidates if os.path.exists(p)), None)
    try:
        if chrome:
            subprocess.Popen([chrome, url], shell=False)
        else:
            webbrowser.open(url)
        return True
    except Exception as e:
        print("Chrome:", e)
        return False

def whatsapp_web():
    return open_chrome("https://web.whatsapp.com/")

def google_search(query):
    import urllib.parse
    q = urllib.parse.quote_plus(str(query).strip())
    return open_chrome("https://www.google.com/search?q=" + q)

def youtube_search(query):
    import urllib.parse
    q = urllib.parse.quote_plus(str(query).strip())
    return open_chrome("https://www.youtube.com/results?search_query=" + q)

def whatsapp_chat(phone=None):
    if phone:
        digits = "".join(ch for ch in str(phone) if ch.isdigit())
        if digits:
            return open_chrome("https://wa.me/" + digits)
    return whatsapp_web()
