from pathlib import Path
from src.editDB.dbFunctions import getRoomId, addRoom, deleteRoom, updateCapacity, getAllRooms

project_root = Path(__file__).parent


# Tests all the functions in one by making sure they all return a rowcount meaning they did a function
def test_all_room_functions():
    # This is the test database
    dbPath = str(project_root) + "/TestingFiles/testDB.sqlite3"
    roomName = "TestRoom"
    capacity = 10
    assert addRoom(roomName, capacity, dbPath) != 0
    roomId = getRoomId(roomName, capacity, dbPath)
    assert roomId
    newCapacity = getRoomId(roomName, capacity, dbPath)
    assert updateCapacity(roomId, newCapacity, dbPath) != 0
    assert deleteRoom(roomId, dbPath) != 0


# Checks to make sure the query to grab all rooms outputs
def test_get_rooms():
    dbPath = str(project_root) + "/TestingFiles/testDB.sqlite3"
    assert getAllRooms(dbPath)