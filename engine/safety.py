import threading

_pending = None
_lock = threading.Lock()

DANGEROUS = {'shutdown', 'restart', 'delete', 'send_message', 'send_audio'}


def request(action, payload=None):
    global _pending
    with _lock:
        _pending = {'action': action, 'payload': payload}
    return _pending


def consume_confirmation(text):
    global _pending
    t = str(text).strip().lower()
    yes = {'yes', 'haan', 'ha', 'confirm', 'confirmed', 'do it', 'kar do', 'bhej do', 'delete kar do'}
    no = {'no', 'nahi', 'cancel', 'stop', 'mat karo'}
    with _lock:
        if not _pending: return None
        if t in no:
            _pending = None; return ('cancel', None)
        if t in yes:
            p = _pending; _pending = None; return ('confirm', p)
    return None


def clear():
    global _pending
    with _lock: _pending = None
