from pathlib import Path
from src.editDB.dbFunctions import getRoomId, addRoom, deleteRoom, updateCapacity


project_root = Path(__file__).parent


# Tests all the functions in one by making sure they all return a rowcount
def test_all_room_functions():
    roomName = "TestRoom"
    capacity = 10
    assert addRoom(roomName, capacity) != 0
    roomId = getRoomId(roomName, capacity)
    assert roomId
    newCapacity = getRoomId(roomName, capacity)
    assert updateCapacity(roomId, newCapacity) != 0
    assert deleteRoom(roomId)!= 0

