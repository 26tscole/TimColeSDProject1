import sqlite3
from pathlib import Path
import csv

DBPath = Path(__file__).resolve().parent.parent.parent / "db.sqlite3"

def DBConnection(path: str | None = None):
    return sqlite3.connect(path)


def getAllRooms(path):
    with DBConnection(path) as conn:
        query = (
            "SELECT id, room_name, capacity FROM booking_meetingroom WHERE is_active"
        )
        return conn.execute(query).fetchall()


def getRoomId(roomName, capacity, path):
    rooms = getAllRooms(path)
    for room in rooms:
        if room[1] == roomName and room[2] == capacity:
            return room[0]
    return None


def saveDeletedReservations(reservations, roomId):
    if not reservations:
        return

    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / f"deletedReservationsForRoom{roomId}.csv"

    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Start_Time",
                "End_Time",
                "no_of_persons",
                "booked_by_id",
                "meeting_room_id",
            ]
        )
        writer.writerows(reservations)
        f.flush()

    print(f"Saved: {file_path}")


def addRoom(roomName, Capacity, path):
    with DBConnection(path) as conn:
        cur = conn.cursor()
        query = "INSERT INTO booking_meetingroom (room_name, capacity, is_active) VALUES (?, ?, 1)"
        cur.execute(query, (roomName, Capacity))
        conn.commit()
        return cur.rowcount


def deleteRoom(roomId, path):
    reservations = []
    row = 0
    with DBConnection(path) as conn:
        cur = conn.cursor()
        bookedRoomsQuery = (
            "SELECT start_time, end_time, no_of_persons, booked_by_id, meeting_room_id "
            "FROM booking_bookinghistory "
            "WHERE meeting_room_id = ?"
        )
        reservations = conn.execute(bookedRoomsQuery, (roomId,)).fetchall()
        deleteBookedRooms = (
            "DELETE FROM booking_bookinghistory WHERE meeting_room_id = ?"
        )
        cur.execute(deleteBookedRooms, (roomId,))
        deleteRoomQuery = "DELETE FROM booking_meetingroom WHERE id = ?"
        cur.execute(deleteRoomQuery, (roomId,))
        conn.commit()
        row = cur.rowcount
    saveDeletedReservations(reservations, roomId)
    return row


def updateCapacity(roomId, capacity, path):
    with DBConnection(path) as conn:
        cur = conn.cursor()
        query = "UPDATE booking_meetingroom SET capacity = ? WHERE id = ?"
        cur.execute(query, (capacity, roomId))
        conn.commit()
        return cur.rowcount
