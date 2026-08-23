from engine.web_automation import open_chrome, whatsapp_web, whatsapp_chat, google_search, youtube_search

def handle_web_command(query, speak):
    q = str(query).strip()
    low = q.lower()

    if low in ("open chrome", "start chrome"):
        speak("Chrome khol rahi hoon Mayank Sir.")
        return open_chrome()

    if low in ("open whatsapp", "open whatsapp web", "whatsapp"):
        speak("WhatsApp Web khol rahi hoon Mayank Sir.")
        return whatsapp_web()

    if low.startswith("google search "):
        term = q[len("google search "):].strip()
        if term:
            speak(f"Google par {term} search kar rahi hoon.")
            return google_search(term)

    if low.startswith("search google for "):
        term = q[len("search google for "):].strip()
        if term:
            speak(f"Google par {term} search kar rahi hoon.")
            return google_search(term)

    if low.startswith("youtube search "):
        term = q[len("youtube search "):].strip()
        if term:
            speak(f"YouTube par {term} search kar rahi hoon.")
            return youtube_search(term)

    if low.startswith("search youtube for "):
        term = q[len("search youtube for "):].strip()
        if term:
            speak(f"YouTube par {term} search kar rahi hoon.")
            return youtube_search(term)

    if low.startswith("whatsapp number "):
        phone = q[len("whatsapp number "):].strip()
        speak("WhatsApp chat open kar rahi hoon.")
        return whatsapp_chat(phone)

    return None
