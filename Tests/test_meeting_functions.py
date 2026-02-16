from pathlib import Path
from src.meetIngActions.users import Users
from datetime import datetime


project_root = Path(__file__).parent


# tests if logging in gives a token
def test_login():
    testUser = Users()
    token = testUser.login()
    assert token


# tests to make sure we can get meeting rooms
def test_available_rooms():
    testUser = Users()
    startTime = "2026-01-01 10:00 AM"
    endTime = "2027-01-01 10:00 AM"
    testRooms = testUser.getAvailableMeetings(startTime=startTime, endTime=endTime)
    assert testRooms



def test_create_meeting():
    roomId = 11
    startTime = "9819-01-01 10:00 AM"
    endTime = "9819-01-01 10:15 AM"
    testUser = Users()
    bookId = testUser.bookMeeting(roomId=roomId, startTime=startTime, endTime=endTime)
    assert bookId
    assert not testUser.bookMeeting(roomId=roomId, startTime=startTime, endTime=endTime)
    testUser.deleteBooking(bookId=bookId)
