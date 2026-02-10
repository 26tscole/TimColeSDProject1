from vosk import Model, KaldiRecognizer
from pathlib import Path
import pyaudio as pa
import wave
import json

modelPath = "vosk-model-small-en-us-0.15"

# checks audio source and then calls audioConversion to turn it into text
# i kind of hate this name
def audioSource(audioFilePath = "", source="microphone", txtFileName="DefaultText.txt"):
    # clears file if it already exists
    # ill probably give a prompt to the user if they want to clear or change the
    # filename but that's not important right now
    with open(txtFileName, 'w') as f:
        f.write("")
    project_root = Path(__file__).parent.parent.parent
    audioFilePath = str(project_root / audioFilePath)
    newModelPath = str(project_root / modelPath)
    model = Model(newModelPath)
    recognizer = None

    # checks the source so we can test the audio file as well
    if source == "microphone":
        mic = pa.PyAudio()
        stream = mic.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()
        recognizer = KaldiRecognizer(model, 16000)
        while True:
            data = stream.read(4000)
            if audioConversion(txtFileName=txtFileName, data=data, recognizer=recognizer): break

    # this is where the audio file should go through
    elif source == "file":
        with wave.open(audioFilePath, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                print("Audio file must be WAV format mono PCM.")
                return
            recognizer = KaldiRecognizer(model, wf.getframerate())
            while True:
                data = wf.readframes(4000)
                if audioConversion(txtFileName = txtFileName, data=data, recognizer=recognizer): break

    # the last result works very strange so I had to add this to actually output it
    final_result = json.loads(recognizer.FinalResult())
    final_text = final_result.get("text", "")
    if final_text:
        outputToFile(txtFileName = txtFileName,audioText = final_text)
        print(final_text)

# this will return true or false depending on whether the recording should end or not
def audioConversion(txtFileName, data, recognizer):
    if len(data) == 0:
        return True
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print(result["text"])
        if result:
            outputToFile(txtFileName = txtFileName,audioText = result["text"])
            if result["text"] == "stop recording" :
                return True
    return False

# sends text to a file or creates a file
def outputToFile(txtFileName="", audioText =""):
    with open(txtFileName, "a") as f:
        f.write(audioText + "\n")