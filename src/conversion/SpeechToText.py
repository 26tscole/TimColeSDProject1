from vosk import Model, KaldiRecognizer
import pyaudio as pa
print(pa)
model = Model("/TimColeSDProject1/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
mic = pa.PyAudio()
stream = mic.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
while stream.is_active():
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text)