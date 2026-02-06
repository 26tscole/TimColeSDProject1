from vosk import Model, KaldiRecognizer
from pathlib import Path
import pyaudio as pa
import wave
import json

modelPath = "vosk-model-small-en-us-0.15"

def audioConversion(source = "microphone", txtFileName="DefaultText.txt", audioFilePath = ""):
    project_root = Path(__file__).parent.parent.parent
    audioFilePath = str(project_root / audioFilePath)
    newModelPath = str(project_root / modelPath)
    model = Model(newModelPath)
    # clears file if it already exists
    # ill probably give a prompt to the user if they want to clear or change the filename but that's not important right now
    with open(txtFileName, 'w') as f:
        f.write("")
    # checks the source a mic or wav file
    if source == "file":
        with wave.open(audioFilePath, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                print("Audio file must be WAV format mono PCM.")
                return
            rec = KaldiRecognizer(model, wf.getframerate())
            while True:
                data = wf.readframes(4000)
                # checks if audio is done
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    print(result.get("text", ""))
                    if result:
                        outputToFile(txtFileName = txtFileName,audioText = result["text"])
            # the last result works very strange so I had to add this to actually output it
            final_result = json.loads(rec.FinalResult())
            final_text = final_result.get("text", "")
            if final_text:
                outputToFile(txtFileName = txtFileName,audioText = final_text)
                print(final_text)
    elif source == "microphone":
        mic = pa.PyAudio()
        stream = mic.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()
        rec = KaldiRecognizer(model, 16000)
        while True:
            data = stream.read(4096)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print(result["text"])
                if result:
                    outputToFile(txtFileName = txtFileName,audioText = result["text"])
                    if result["text"] == "stop recording":
                        break

        final_result = json.loads(rec.FinalResult())
        final_text = final_result.get("text", "")
        if final_text:
            outputToFile(txtFileName=txtFileName, audioText=final_text)
            print(final_text)

def outputToFile(txtFileName="", audioText =""):
    with open(txtFileName, "a") as f:
        f.write(audioText + "\n")


