import subprocess, ctypes, webbrowser, platform

def open_app(name):
    aliases={"notepad":"notepad.exe","calculator":"calc.exe","calc":"calc.exe","paint":"mspaint.exe","explorer":"explorer.exe","file explorer":"explorer.exe"}
    try:
        subprocess.Popen(aliases.get(name.lower().strip(), name), shell=True)
        return True
    except Exception as e:
        print("open_app:", e); return False

def close_app(name):
    aliases={"notepad":"notepad.exe","calculator":"CalculatorApp.exe","calc":"CalculatorApp.exe","paint":"mspaint.exe"}
    exe=aliases.get(name.lower().strip(), name if name.lower().endswith(".exe") else name+".exe")
    try:
        subprocess.run(["taskkill","/IM",exe,"/F"],capture_output=True); return True
    except Exception as e:
        print("close_app:", e); return False

def lock_pc():
    try: ctypes.windll.user32.LockWorkStation(); return True
    except Exception as e: print("lock_pc:",e); return False

def shutdown_pc(delay=10):
    try: subprocess.run(["shutdown","/s","/t",str(delay)],capture_output=True); return True
    except Exception as e: print("shutdown:",e); return False

def restart_pc(delay=10):
    try: subprocess.run(["shutdown","/r","/t",str(delay)],capture_output=True); return True
    except Exception as e: print("restart:",e); return False

def cancel_power():
    try: subprocess.run(["shutdown","/a"],capture_output=True); return True
    except Exception as e: print("cancel:",e); return False

def system_info():
    return {"OS":platform.platform(),"Processor":platform.processor() or "Unknown","Python":platform.python_version()}
