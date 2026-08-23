# 🤖 MS_AI — Intelligent AI Assistant

<p align="center">
  <b>⚡ Smart • Voice Controlled • AI Powered • Modern</b>
</p>

<p align="center">
  An advanced AI assistant built with Python, featuring voice interaction, face authentication, intelligent responses, automation, and a modern futuristic interface.
</p>

---

## ✨ About MS_AI

**MS_AI** is an intelligent personal AI assistant designed to provide a futuristic assistant experience using **Python, Artificial Intelligence, Voice Recognition, Text-to-Speech, Face Authentication, and Web Technologies**.

The project combines a powerful Python backend with a modern interactive interface to create a smart and responsive AI assistant.

> 🧠 **Think Smart. Speak Naturally. Automate Everything.**

---

## 🚀 Key Features

* 🤖 AI-powered intelligent responses
* 🎙️ Voice command recognition
* 🔊 Natural Text-to-Speech responses
* 👤 Face authentication system
* 🧠 Smart assistant interaction
* 🌐 Modern web-based interface
* ⚡ Fast and responsive UI
* 🎨 Futuristic assistant design
* 🖥️ Desktop automation support
* 🔐 Authentication-based access
* 🎵 Assistant sound effects
* 📡 Internet-based AI capabilities
* 💬 Continuous voice interaction
* 🧩 Modular project structure
* 🛠️ Easy to customize and extend

---

## 🧠 Technology Stack

| Technology             | Purpose                         |
| ---------------------- | ------------------------------- |
| 🐍 Python              | AI & Core Logic                 |
| 🎙️ Speech Recognition | Voice Input                     |
| 🔊 pyttsx3             | Text-to-Speech                  |
| 👁️ OpenCV             | Face Detection & Authentication |
| 🌐 HTML5               | Frontend Structure              |
| 🎨 CSS3                | UI & Styling                    |
| ⚡ JavaScript           | Frontend Interaction            |
| 🧠 AI Models / APIs    | Intelligent Responses           |

---

## 📁 Project Structure

```text
jarvis-main/
│
├── engine/
│   ├── auth/
│   │   ├── samples/
│   │   │   ├── face.1.1.jpg
│   │   │   ├── face.1.2.jpg
│   │   │   ├── ...
│   │   │   └── face.1.50.jpg
│   │   │
│   │   ├── trainer/
│   │   │   └── trainer.yml
│   │   │
│   │   ├── haarcascade_frontalface_default.xml
│   │   ├── recognize.py
│   │   └── trainer.py
│   │
│   ├── __init__.py
│   ├── advanced_commands.py
│   ├── automation.py
│   ├── automation_commands.py
│   ├── browser_control.py
│   ├── command.py
│   ├── config.py
│   ├── contact_whatsapp.py
│   ├── contact_whatsapp_commands.py
│   ├── db.py
│   ├── features.py
│   ├── helper.py
│   ├── local_commands.py
│   ├── memory.json
│   ├── memory.py
│   ├── ms_memory.py
│   ├── pc_advanced.py
│   ├── pc_commands.py
│   ├── pc_control.py
│   ├── safety.py
│   ├── smart_intent.py
│   ├── tts.py
│   ├── v14_commands.py
│   ├── v14_macros.py
│   ├── v14_screen.py
│   ├── voice_config.py
│   ├── voice_notes.py
│   ├── web_automation.py
│   ├── web_commands.py
│   ├── whatsapp_commands.py
│   ├── whatsapp_send.py
│   └── whatsapp_smart.py
│
├── www/
│   ├── assets/
│   │   ├── audio/
│   │   │   └── start_sound
│   │   │
│   │   ├── img/
│   │   │   └── logo
│   │   │
│   │   └── vendor/
│   │       └── textillate/
│   │           ├── animate.css
│   │           ├── jquery.fittext.js
│   │           ├── jquery.lettering.js
│   │           └── style.css
│   │
│   ├── controller.js
│   ├── index.html
│   ├── main.js
│   ├── script.js
│   └── style.css
│
├── jarvis.db
├── main.py
├── requirements.txt
└── VOICE_SETUP.md
```

### 🧩 Core Components

| Folder / File                 | Purpose                                     |
| ----------------------------- | ------------------------------------------- |
| `engine/`                     | Core AI assistant logic                     |
| `engine/auth/`                | Face authentication system                  |
| `engine/advanced_commands.py` | Advanced assistant commands                 |
| `engine/automation.py`        | System automation                           |
| `engine/browser_control.py`   | Browser control & automation                |
| `engine/memory.py`            | Assistant memory system                     |
| `engine/pc_control.py`        | PC control functionality                    |
| `engine/smart_intent.py`      | Smart command & intent detection            |
| `engine/tts.py`               | Text-to-Speech functionality                |
| `engine/whatsapp_smart.py`    | WhatsApp automation                         |
| `www/`                        | Web-based assistant interface               |
| `www/assets/`                 | UI assets, images, audio & vendor libraries |
| `jarvis.db`                   | Local database                              |
| `main.py`                     | Main application entry point                |
| `requirements.txt`            | Python dependencies                         |
| `VOICE_SETUP.md`              | Voice configuration & setup guide           |


> 📌 Folder names may vary depending on your latest project version.

---

## ⚙️ Requirements

Before running MS_AI, make sure you have:

* Python 3.10+
* Windows / compatible operating system
* Working microphone
* Webcam for face authentication
* Internet connection for online AI features

---

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/cyber-mayank447/MS_AI-.git
```

### 2️⃣ Open Project Folder

```bash
cd MS_AI-
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run MS_AI

```bash
python ms_ai.py
```

---

## 🎙️ Voice Assistant

MS_AI can interact with the user through voice commands.

The basic flow is:

```text
🎙️ User Voice
      ↓
🧠 Speech Recognition
      ↓
🤖 AI Processing
      ↓
💡 Response Generation
      ↓
🔊 Text-to-Speech
      ↓
🎧 Voice Response
```

---

## 👤 Face Authentication

MS_AI includes a face authentication system using **OpenCV**.

The authentication system can:

1. Detect a face using Haar Cascade.
2. Process the detected face.
3. Compare it with the trained model.
4. Authenticate the user.
5. Allow access to the assistant.

```text
📷 Camera
   ↓
👁️ Face Detection
   ↓
🧠 Face Recognition
   ↓
🔐 Authentication
   ↓
🤖 MS_AI Access
```

---

## 🎨 User Interface

The project includes a modern assistant interface designed around a futuristic AI concept.

### UI Highlights

* Futuristic dark interface
* Animated assistant elements
* Voice listening indicators
* Interactive buttons
* Responsive layout
* Smooth animations
* Modern typography
* Glass-style UI elements

---

## 🔐 Security

MS_AI can use face authentication as an additional access-control layer.

**Important:** Keep trained face data and authentication files private if you plan to distribute the project.

---

## 📦 Dependencies

Main Python libraries may include:

```text
opencv-python
pyttsx3
SpeechRecognition
PyAutoGUI
Flask
Flask-CORS
PyAudio
```

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## 🧪 Development

Want to customize MS_AI?

You can modify:

```text
engine/        → AI & assistant logic
static/css/    → UI design
static/js/     → Frontend interaction
templates/     → Web interface
ms_ai.py       → Main application
```

---

## 🔮 Future Roadmap

Planned improvements for MS_AI may include:

* [ ] Wake-word detection
* [ ] Continuous conversation mode
* [ ] Better natural-language understanding
* [ ] Advanced AI model integration
* [ ] Improved face recognition
* [ ] Bluetooth headset support
* [ ] Smart device control
* [ ] Android version
* [ ] Cloud-based AI processing
* [ ] Personalized assistant memory
* [ ] More automation features
* [ ] Advanced futuristic HUD interface

---

## ⚠️ Disclaimer

MS_AI is a personal AI assistant project created for **learning, experimentation, automation, and development purposes**.

Some features may require additional configuration, API keys, hardware, drivers, or third-party services.

---

## 👨‍💻 Developer

### **Mayank Prajapat**

Building futuristic AI projects with:

**Python • AI • Automation • Web Technologies • Computer Vision**

---

## ⭐ Support

If you find **MS_AI** interesting or useful:

⭐ Star the repository
🍴 Fork the project
🐛 Report bugs
💡 Suggest new features
📢 Share the project

---

## 📜 License

This project is provided for educational and personal development purposes.

---

<p align="center">

### 🤖 MS_AI

**"Your Assistant. Your Intelligence. Your Future."**

⭐ Made with Python & AI

</p>
