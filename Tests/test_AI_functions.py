from pathlib import Path
import pytest
from src.AIconnection.agent import runAIChat
from src.meetIngActions.users import Users

project_root = Path(__file__).parent


@pytest.fixture
def test_user_booking():
    roomId = 1
    startTime = "2040-01-01 10:00 AM"
    endTime = "2040-01-01 10:15 AM"
    testUser = Users()
    bookId = testUser.bookMeeting(roomId=roomId, startTime=startTime, endTime=endTime)
    yield
    testUser.deleteBooking(bookId=bookId)


def test_runAIChat(test_user_booking):
    audioFilePath = str(project_root) + "/TestingFiles/AIAudioTest.wav"
    response = runAIChat(source="file", audioFilePath=audioFilePath)
    assert response
    foundStartTime = response[0]["data"][0]["start_time"]
    foundEndTime = response[0]["data"][0]["end_time"]
    assert foundStartTime == "2040-01-01T10:00:00Z"
    assert foundEndTime == "2040-01-01T10:15:00Z"
