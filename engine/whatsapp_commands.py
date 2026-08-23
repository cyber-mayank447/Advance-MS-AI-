import re
from engine.whatsapp_send import send_message

def _extract_command(query):
    q = str(query).strip()

    # Supported:
    # whatsapp send 919876543210 hello bhai
    # send whatsapp to 919876543210 hello bhai
    patterns = [
        r"^whatsapp\s+send\s+(\+?\d[\d\s-]{6,})\s+(.+)$",
        r"^send\s+whatsapp\s+to\s+(\+?\d[\d\s-]{6,})\s+(.+)$",
        r"^send\s+message\s+to\s+(\+?\d[\d\s-]{6,})\s+(.+)$",
    ]
    for p in patterns:
        m = re.match(p, q, re.I)
        if m:
            phone = "".join(ch for ch in m.group(1) if ch.isdigit())
            message = m.group(2).strip()
            if len(phone) >= 7 and message:
                return phone, message
    return None

def handle_whatsapp_command(query, speak):
    parsed = _extract_command(query)
    if not parsed:
        return None

    phone, message = parsed
    speak("Theek hai Mayank Sir, WhatsApp message send kar rahi hoon.")
    try:
        result = send_message(phone, message)
        if result:
            speak("Message send command complete, Mayank Sir.")
        else:
            speak("Sorry Mayank Sir, number ya message valid nahi mila.")
        return result
    except Exception as e:
        print("WhatsApp send error:", e)
        speak("Sorry Mayank Sir, WhatsApp message send nahi ho paya.")
        return False
