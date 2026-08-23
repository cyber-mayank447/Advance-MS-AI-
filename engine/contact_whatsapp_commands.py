import re
from engine.contact_whatsapp import send_to_contact

def _parse(query):
    q = str(query).strip()

    patterns = [
        r"^whatsapp\s+send\s+to\s+(.+?)\s+(.+)$",
        r"^send\s+whatsapp\s+to\s+(.+?)\s+(.+)$",
        r"^whatsapp\s+message\s+to\s+(.+?)\s+(.+)$",
    ]

    for pattern in patterns:
        m = re.match(pattern, q, re.I)
        if m:
            return m.group(1).strip(), m.group(2).strip()
    return None

def handle_contact_whatsapp_command(query, speak):
    parsed = _parse(query)
    if not parsed:
        return None

    name, message = parsed
    result = send_to_contact(name, message)

    if result is None:
        speak(f"Mayank Sir, {name} naam ka contact nahi mila. Pehle Contacts mein save kar do.")
        return False

    contact, sent = result
    if sent:
        speak(f"Theek hai Mayank Sir, {contact['name']} ko WhatsApp message send kar diya.")
    else:
        speak(f"Sorry Mayank Sir, {contact['name']} ko message send nahi ho paya.")
    return sent
