import os
import subprocess
import eel


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "PASTE_YOUR_NEW_GEMINI_API_KEY_HERE")

if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("PASTE_"):
    
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

from engine.features import *
from engine.command import *
from engine.auth import recoganize


def start():
    print("================================")
    print("MS STARTING...")
    print("================================")

    # API status
    if GEMINI_API_KEY.startswith("PASTE_") or not GEMINI_API_KEY.strip():
        print("WARNING: Gemini API key is not configured.")
        print("Open main.py and paste your NEW Gemini API key in GEMINI_API_KEY.")
    else:
        print("Gemini API key configured.")

    eel.init("www")

    print("Eel initialized")

    try:
        playAssistantSound()
        print("Assistant sound played")
    except Exception as e:
        print("Sound Error:", e)

    @eel.expose
    def init():
        print("Face authentication started...")

        try:
            # ADB/device.bat temporarily disabled
            # subprocess.call([r'device.bat'])

            eel.hideLoader()

            speak("Ready for Face Authentication")

            flag = recoganize.AuthenticateFace()

            print("Face Authentication Result:", flag)

            if flag == 1:

                eel.hideFaceAuth()

                speak("Face Authentication Successful")

                eel.hideFaceAuthSuccess()

                speak("Hello Mayank Sir, welcome back. How can I help you?")

                eel.hideStart()

                playAssistantSound()

            else:
                speak("Face Authentication Failed")

        except Exception as e:
            print("Face Authentication Error:", e)

    print("Starting MS UI...")

    eel.start(
        'index.html',
        mode='brave',
        host='localhost',
        port=8000,
        block=True
    )


if __name__ == "__main__":
    print("MAIN FILE EXECUTED")
    start()
