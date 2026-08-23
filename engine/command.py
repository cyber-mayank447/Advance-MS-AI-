import time
import eel
import speech_recognition as sr

from engine.smart_intent import handle_smart_intent
from engine.whatsapp_smart import handle as handle_whatsapp_smart
from engine.web_commands import handle_web_command
from engine.advanced_commands import handle as handle_advanced
from engine.pc_commands import handle_pc_command
from engine.safety import consume_confirmation, request
from engine.v14_commands import handle_v14_command


def speak(text):
    text = str(text).strip()
    if not text:
        return
    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)
    except Exception:
        pass
    from engine.tts import speak as tts_speak
    tts_speak(text)


def takecommand():
    r=sr.Recognizer(); r.pause_threshold=0.8
    with sr.Microphone() as source:
        print('Listening for Mayank Sir...')
        try: eel.DisplayMessage('Listening...')
        except Exception: pass
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio=r.listen(source, timeout=10, phrase_time_limit=15)
    try:
        eel.DisplayMessage('Recognizing...')
        query=r.recognize_google(audio, language='en-IN')
        print('USER:', query); eel.DisplayMessage(query)
        return query.strip()
    except sr.UnknownValueError:
        speak("Mujhe samajh nahi aaya Mayank Sir. Ek baar phir bol do."); return ''
    except sr.RequestError:
        speak('Speech recognition service abhi available nahi hai.'); return ''
    except Exception as e:
        print('Speech error:',e); return ''


def _execute_pending(pending):
    action= pending['action']; payload=pending.get('payload') or {}
    if action=='send_message':
        from engine.whatsapp_send import send_message
        return send_message(payload['contact']['phone'], payload['message'])
    if action=='delete':
        from engine.pc_advanced import delete_path
        return delete_path(payload['path'])
    if action=='shutdown':
        from engine.pc_control import shutdown_pc
        return shutdown_pc(10)
    if action=='restart':
        from engine.pc_control import restart_pc
        return restart_pc(10)
    return False


def _handle_confirmations(query):
    result=consume_confirmation(query)
    if not result: return None
    status,pending=result
    if status=='cancel': speak('Theek hai Mayank Sir, action cancel kar diya.'); return True
    ok=_execute_pending(pending)
    if pending['action']=='send_message': speak('WhatsApp message send kar diya Mayank Sir.' if ok else 'Message send nahi ho paya.')
    elif pending['action']=='delete': speak('Delete complete Mayank Sir.' if ok else 'Delete nahi ho paya.')
    elif pending['action']=='shutdown': speak('PC 10 seconds mein shutdown hoga Mayank Sir.')
    elif pending['action']=='restart': speak('PC 10 seconds mein restart hoga Mayank Sir.')
    return True


@eel.expose
def allCommands(message=1):
    query=takecommand() if message==1 else str(message).strip()
    if message!=1:
        try: eel.senderText(query)
        except Exception: pass
    if not query: return
    try:
        # Keep a short local conversation trail for context-aware commands.
        try:
            from engine.memory import remember as remember_context
            remember_context(query)
        except Exception: pass
        # Highest priority: confirmation for a previously requested sensitive action.
        if _handle_confirmations(query) is not None: return

        for handler in (
            lambda q: handle_v14_command(q,speak),
            lambda q: handle_advanced(q,speak),
            lambda q: handle_whatsapp_smart(q,speak),
            lambda q: handle_smart_intent(q,speak),
            lambda q: handle_web_command(q,speak),
            lambda q: handle_pc_command(q,speak),
        ):
            result=handler(query)
            if result is not None: return

        # Legacy commands remain available.
        from engine.local_commands import handle_local_command
        if handle_local_command(query): return
        try:
            from engine.features import geminai
            geminai(query)
        except Exception as e:
            print('AI fallback error:',e)
            speak('Sorry Mayank Sir, command samajh nahi aayi.')
    except Exception as e:
        print('Command error:',e); speak('Sorry Mayank Sir, kuch problem aa gayi.')
    finally:
        try: eel.ShowHood()
        except Exception: pass
