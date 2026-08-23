import re
from engine.contact_whatsapp import find_contacts
from engine.whatsapp_send import send_message
from engine.safety import request
from engine.web_automation import whatsapp_web, whatsapp_chat


def _extract(q):
    patterns=[
      r'^(?:send|bhej|send a)\s+(?:a\s+)?(?:whatsapp\s+)?(?:message|msg)\s+to\s+(.+?)\s+(?:saying|that|ki)\s+(.+)$',
      r'^(.+?)\s+ko\s+(?:bol de|message bhej do|msg bhej do|message bhejo|msg bhejo)\s+(.+)$',
      r'^(.+?)\s+ko\s+(?:keh do|bata do)\s+(.+)$',
    ]
    for p in patterns:
        m=re.match(p,q.strip(),re.I)
        if m: return m.group(1).strip(),m.group(2).strip()
    return None


def handle(query, speak):
    q=str(query).strip()
    low=q.lower()
    if low in ('open whatsapp','whatsapp kholo','whatsapp khol'):
        speak('Haan Mayank Sir, WhatsApp Web khol rahi hoon.'); return whatsapp_web()
    if 'last message' in low or 'last msg' in low or 'last message kya aaya' in low or 'aakhri message' in low:
        speak('WhatsApp Web mein chat open kar sakti hoon, lekin exact last-message reading ke liye browser DOM integration chahiye.'); return whatsapp_web()
    parsed=_extract(q)
    if not parsed: return None
    name,message=parsed
    contacts=find_contacts(name)
    if not contacts:
        speak(f'Mayank Sir, {name} naam ka contact nahi mila.'); return False
    if len(contacts)>1:
        labels=' ya '.join(c['name'] for c in contacts[:5])
        speak(f'Mayank Sir, multiple contacts mile: {labels}. Exact naam bol do.')
        return False
    contact=contacts[0]
    request('send_message', {'contact':contact,'message':message})
    speak(f'{contact["name"]} ko ye message bhejna hai: {message}. Confirm bolo.')
    return 'WAIT_CONFIRM'
