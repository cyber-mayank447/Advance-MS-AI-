import os, time, wave
from pathlib import Path

try:
    import pyaudio
except Exception:
    pyaudio = None

VOICE_DIR = Path(os.path.expanduser('~/Documents/MS_VoiceNotes'))


def record_voice(seconds=10, rate=16000):
    if pyaudio is None: raise RuntimeError('PyAudio is not installed')
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    path = VOICE_DIR / f'voice_{time.strftime("%Y%m%d_%H%M%S")}.wav'
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=1024)
    frames=[]
    try:
        for _ in range(max(1, int(rate/1024*seconds))): frames.append(stream.read(1024, exception_on_overflow=False))
    finally:
        stream.stop_stream(); stream.close(); pa.terminate()
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16)); wf.setframerate(rate); wf.writeframes(b''.join(frames))
    return str(path)
