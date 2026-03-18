import sqlite3
from pathlib import Path

def DBConnection():
    DBPath = Path(__file__).resolve().parent.parent.parent / "db.sqlite3"
    return sqlite3.connect(DBPath)

def getAllRooms():
    with DBConnection() as conn:
        query = "SELECT id, room_name, capacity FROM booking_meetingroom WHERE is_active"
        return conn.execute(query).fetchall()


def addRoom(roomName, Capacity):
    with DBConnection() as conn:
        cur = conn.cursor()
        query = "INSERT INTO booking_meetingroom (room_name, capacity, is_active) VALUES (?, ?, 1)"
        cur.execute(query, (roomName, Capacity))
        conn.commit()
        return cur.fetchall()

def deleteRoom(roomId):
    with DBConnection() as conn:
        bookedRoomsQuery="SELECT * FROM booking_bookinghistory WHERE meeting_room_id=?"
        bookedRooms = conn.execute(bookedRoomsQuery, (roomId,)).fetchall()
        deleteBookedRooms = "DELETE FROM booking_bookinghistory WHERE id = ?"
        conn.execute(deleteBookedRooms, (roomId,))
        deleteRoomQuery="DELETE FROM booking_meetingroom WHERE id = ?"
        conn.execute(deleteRoomQuery, (roomId,))
        conn.commit()
        return bookedRooms

def updateCapacity(roomId, capacity):
    with DBConnection() as conn:
        cur = conn.cursor()
        query = "UPDATE booking_meetingroom SET capacity = ? WHERE id = ?"
        cur.execute(query, (capacity, roomId))
        conn.commit()
        return cur.rowcount

