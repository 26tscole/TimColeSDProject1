from pathlib import Path
from src.conversion.SpeechToText import audioSource

project_root = Path(__file__).parent


# tests if audio is being converted and saved to a file correctly
def test_audio_conversion():
    audioFilePath = str(project_root) + "/TestingFiles/testAudio.wav"
    expectedAudioOutput = str(project_root) + "/TestingFiles/ExpectedOutputText.txt"
    generatedAudioOutput = "generatedText.txt"

    audioSource(
        source="file", audioFilePath=audioFilePath, txtFileName="generatedText.txt"
    )

    with open(generatedAudioOutput) as f:
        actual_text = f.read().strip()

    with open(expectedAudioOutput) as f:
        expected_text = f.read().strip()

    assert (
        actual_text == expected_text
    ), f"Mismatch:\nExpected: {expected_text}\nActual: {actual_text}"
