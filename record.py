import sounddevice as sd
import wavio

def record_audio(file_path, duration=10, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wavio.write(file_path, audio, fs, sampwidth=2)
    print("Recording finished and saved to", file_path)
