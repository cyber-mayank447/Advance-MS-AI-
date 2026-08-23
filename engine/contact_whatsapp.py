import os, sqlite3
from engine.whatsapp_send import send_message


def _db_path(): return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jarvis.db')


def find_contacts(name):
    name = str(name).strip()
    if not name: return []
    con=sqlite3.connect(_db_path()); cur=con.cursor()
    try:
        cur.execute('''SELECT name, mobile_no FROM contacts WHERE lower(name)=lower(?) OR lower(name) LIKE lower(?) ORDER BY id DESC''', (name, '%'+name+'%'))
        rows=cur.fetchall()
    finally: con.close()
    out=[]
    for n,p in rows:
        phone=''.join(ch for ch in str(p or '') if ch.isdigit())
        if phone: out.append({'name':n,'phone':phone})
    # de-duplicate exact name+phone
    seen=set(); unique=[]
    for x in out:
        k=(x['name'].lower(),x['phone'])
        if k not in seen: seen.add(k); unique.append(x)
    return unique


def find_contact(name):
    rows=find_contacts(name); return rows[0] if rows else None


def send_to_contact(contact, message):
    return send_message(contact['phone'], message)
