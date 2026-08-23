
# ---------------- MS Friendly Hinglish / Marwari Voice ----------------
def ms_sweet_reply(text):
    """Light conversational polishing for MS's spoken replies."""
    text = str(text).strip()
    replacements = {
        "How can I help you?": "Batao Mayank Sir, kya karna hai?",
        "I am sorry": "Sorry Mayank Sir",
        "I don't understand": "Mujhe samajh nahi aaya",
        "I didn't understand": "Mujhe samajh nahi aaya",
        "Please try again": "Ek baar phir bol do",
        "Good morning": "Good morning Mayank Sir, ram ram sa!",
        "Good evening": "Good evening Mayank Sir, ram ram sa!",
        "Good night": "Good night Mayank Sir, aaram se sona.",
        "Done": "Ho gaya Mayank Sir.",
        "Okay": "Theek hai Mayank Sir.",
        "Thank you": "Koi baat nahi Mayank Sir.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
# ----------------------------------------------------------------------


from engine.db import con, cursor
from engine.memory import context
import json
import os
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME, LLM_KEY
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, markdown_to_text, remove_words
from hugchat import hugchat

con = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(__file__)), "jarvis.db"))
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        if os.name == "nt":
                            subprocess.Popen(["cmd", "/c", "start", "", query], shell=False)
                        else:
                            subprocess.Popen([query])
                    except Exception as e:
                        print(f"Open command error: {e}")
                        speak("Mayank Sir, I couldn't find that application.")
        except Exception as e:
            print(f"Open command error: {e}")
            speak("Mayank Sir, something went wrong while opening that.")

       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        # "MS" is not a built-in Porcupine keyword. Use SpeechRecognition
        # for the custom wake word so the assistant can actually listen for "MS".
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("MS hotword listener is ready.")
            while True:
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                    heard = recognizer.recognize_google(audio, language="en-in").lower().strip()
                    if re.search(r"\bms\b", heard):
                        print("MS hotword detected")
                        pyautogui.hotkey("win", "j")
                        time.sleep(1)
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"Hotword recognition error: {e}")
                    time.sleep(2)
                except Exception as e:
                    print(f"Hotword listener error: {e}")
                    time.sleep(1)
        return
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        ms_message = "Message sent successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        ms_message = "Calling "+name

    else:
        target_tab = 6
        message = ''
        ms_message = "Starting video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(ms_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path=os.path.join("engine", "cookies.json"))
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)

import google.generativeai as genai
def geminai(query):
    try:
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")
        # Set your API key
        if not LLM_KEY:
            speak("Mayank Sir, Google AI API key is not configured.")
            return

        genai.configure(api_key=LLM_KEY)

        # Select a model
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Generate a response
        response = model.generate_content("You are MS, Mayank Sir\'s personal AI assistant. Never introduce yourself as Google, Gemini, OpenAI, or another company. If asked who created you, say: \"Mayank Sir ne mujhe banaya hai.\" Reply in natural Hinglish/Marwadi when appropriate. Keep normal answers concise (1-4 sentences) unless the user asks for detail.\nMemory:\n" + context(8) + "\nUser:\n" + query)
        filter_text = markdown_to_text(response.text)
        speak(filter_text)
    except Exception as e:
        print("Gemini error:", e)
        speak("Sorry Mayank Sir, I couldn't process that request.")

# Settings Modal 



# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1    
    except:
        print("no data")


@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            '''UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?''',
            (name, designation, mobileno, email, city)
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            '''INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)''',
            (name, designation, mobileno, email, city)
        )

    con.commit()
    personalInfo()
    return 1



@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command VALUES (?, ?, ?)''', (None,key, value))
    con.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    con.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', (None,Name, MobileNo, Email, City))
    con.commit()
