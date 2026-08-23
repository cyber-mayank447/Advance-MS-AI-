import asyncio
import os
import queue
import subprocess
import tempfile
import threading
import time

VOICE = "en-IN-NeerjaNeural"
_q = queue.Queue(maxsize=10)
_worker_started = False


def _sapi_fallback(text):
    safe = str(text).replace("'", "''")
    ps = f"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Rate = -1
$s.Volume = 100
$voices = $s.GetInstalledVoices() | ForEach-Object {{ $_.VoiceInfo }}
$preferred = @('Microsoft Heera','Microsoft Neerja','Microsoft Zira','Microsoft Jenny','Microsoft Aria')
$selected = $null
foreach ($p in $preferred) {{
  $selected = $voices | Where-Object {{ $_.Name -like \"*$p*\" -and $_.Gender -eq 'Female' }} | Select-Object -First 1
  if ($selected) {{ break }}
}}
if (-not $selected) {{ $selected = $voices | Where-Object {{ $_.Gender -eq 'Female' }} | Select-Object -First 1 }}
if ($selected) {{ $s.SelectVoice($selected.Name); Write-Host \"MS female SAPI voice: $($selected.Name)\" }}
$s.Speak('{safe}')
"""
    try:
        subprocess.run(["powershell","-NoProfile","-ExecutionPolicy","Bypass","-Command",ps],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    except Exception as e:
        print("SAPI voice error:", e)


def _edge_speak(text):
    """Generate Indian female neural speech. Returns True only after audio plays."""
    try:
        import edge_tts
        import winsound

        async def make_audio(path):
            communicate = edge_tts.Communicate(str(text), VOICE, rate="-8%", volume="+0%")
            await communicate.save(path)

        for attempt in range(2):
            fd, path = tempfile.mkstemp(prefix="ms_tts_", suffix=".mp3")
            os.close(fd)
            try:
                asyncio.run(make_audio(path))
                if not os.path.exists(path) or os.path.getsize(path) < 1000:
                    raise RuntimeError("Neural voice returned no audio")
                # Convert MP3 to WAV with ffmpeg if available, then use Windows audio playback.
                wav = path[:-4] + ".wav"
                converted = False
                try:
                    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",path,wav],
                                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20,check=False)
                    converted = os.path.exists(wav) and os.path.getsize(wav) > 1000
                except Exception:
                    pass
                if converted:
                    winsound.PlaySound(wav, winsound.SND_FILENAME)
                    return True
                # playsound is a fallback for systems without ffmpeg.
                from playsound import playsound
                playsound(path)
                return True
            except Exception as e:
                if attempt == 1:
                    print("Neural voice unavailable:", e)
            finally:
                for p in (path, path[:-4] + ".wav"):
                    try: os.remove(p)
                    except OSError: pass
                if attempt == 0:
                    time.sleep(0.4)
    except Exception as e:
        print("Neural voice unavailable:", e)
    return False


def _worker():
    while True:
        text = _q.get()
        try:
            if text:
                if not _edge_speak(text):
                    _sapi_fallback(text)
        except Exception as e:
            print("TTS worker error:", e)
        finally:
            _q.task_done()


def _ensure_worker():
    global _worker_started
    if not _worker_started:
        threading.Thread(target=_worker, daemon=True, name="MS-TTS",).start()
        _worker_started = True


def speak(text):
    text = str(text).strip()
    if not text:
        return
    print("MS:", text)
    _ensure_worker()
    try:
        _q.put_nowait(text)
    except queue.Full:
        print("TTS queue full; skipping speech.")
