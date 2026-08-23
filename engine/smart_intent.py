import re
from engine.ms_memory import remember, recall, forget, summary


def handle_smart_intent(query, speak):
    q=str(query).strip(); low=q.lower()
    m=re.match(r'^(?:remember|yaad rakhna|yaad rakh)\s+(?:that\s+)?my\s+(.+?)\s+is\s+(.+)$',q,re.I)
    if not m: m=re.match(r'^(?:remember|yaad rakhna|yaad rakh)\s+(?:that\s+)?(.+?)\s+is\s+(.+)$',q,re.I)
    if m:
        key,value=m.group(1).strip(),m.group(2).strip(); remember(key,value); speak(f'Theek hai Mayank Sir, {key} yaad rakh liya.'); return True
    if low in ('what do you remember','what do you know about me','mujhe kya yaad hai','meri memory batao'):
        items=summary(); speak('Meri memory mein: '+('; '.join(items[:10]) if items else 'abhi kuch saved nahi hai.')+' Mayank Sir.'); return True
    m=re.match(r'^(?:what is my|mera|meri)\s+(.+?)(?:\?|$)',q,re.I)
    if m:
        key=m.group(1).strip(); value=recall(key); speak(f'Mayank Sir, {key} {value} hai.' if value else f'Mujhe {key} ki saved information nahi mil rahi.'); return True
    m=re.match(r'^(?:forget|bhool jao|bhul jao)\s+(.+)$',q,re.I)
    if m:
        ok=forget(m.group(1).strip()); speak('Theek hai Mayank Sir, bhool gayi.' if ok else 'Woh memory nahi mili.'); return True
    return None
