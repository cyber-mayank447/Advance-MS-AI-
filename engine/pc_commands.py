from engine.pc_control import open_app,close_app,lock_pc,shutdown_pc,restart_pc,cancel_power,system_info
from engine.safety import request

def handle_pc_command(query,speak):
    q=str(query).lower().strip()
    if q in ("open notepad","start notepad"): speak("Notepad khol rahi hoon Mayank Sir."); return open_app("notepad")
    if q in ("open calculator","open calc","start calculator"): speak("Calculator khol rahi hoon Mayank Sir."); return open_app("calculator")
    if q in ("open paint","start paint"): speak("Paint khol rahi hoon Mayank Sir."); return open_app("paint")
    if q in ("open file explorer","open explorer"): speak("File Explorer khol rahi hoon Mayank Sir."); return open_app("explorer")
    if q in ("close notepad","close calculator","close calc","close paint"):
        name=q.replace("close ",""); speak(f"{name} close kar rahi hoon Mayank Sir."); return close_app(name)
    if q in ("lock pc","lock computer","lock my pc"): speak("PC lock kar rahi hoon Mayank Sir."); return lock_pc()
    if q in ("system info","system information","my pc information"):
        i=system_info(); speak(f"Mayank Sir, aapka system {i['OS']} hai aur Python {i['Python']} hai."); return True
    if q in ("cancel shutdown","cancel restart"): speak("Power action cancel kar diya Mayank Sir."); return cancel_power()
    if q in ("shutdown pc","shut down pc","turn off pc"):
        request('shutdown'); speak("Shutdown ready hai. Confirm bolo agar sach mein PC band karna hai."); return "WAIT_CONFIRM"
    if q=="confirm shutdown": request('shutdown'); return 'WAIT_CONFIRM'
    if q in ("restart pc","restart computer"):
        request('restart'); speak("Restart ready hai. Confirm bolo agar restart karna hai."); return "WAIT_CONFIRM"
    if q=="confirm restart": request('restart'); return 'WAIT_CONFIRM'
    return None
