from pathlib import Path
from nicegui import ui
from src.editDB.dbFunctions import (
    getAllRooms,
    addRoom as dbAdd,
    deleteRoom as dbDelete,
    updateCapacity as dbUpdate,
)

DBPath = str(Path(__file__).resolve().parent.parent.parent.parent /"server" / "db.sqlite3")


def checkValidity(items: list[str]):
    isMissing = any(item == "" for item in items)
    print(items)
    if isMissing:
        ui.notify("Cannot Submit: Missing Fields")
        return False
    else:
        ui.notify(f"You entered: {items}")
        return True


def getTableRooms():
    rooms = getAllRooms()
    return [
        {"id": room[0], "room_name": room[1], "capacity": room[2]} for room in rooms
    ]


@ui.refreshable
def roomTable():
    allRooms = getTableRooms()
    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "room_name", "label": "Room Name", "field": "room_name"},
        {"name": "capacity", "label": "Capacity", "field": "capacity"},
    ]
    with ui.card().classes("flex-1 p-4"):
        ui.label("All Available Rooms").classes("text-subtitle1")
        ui.table(columns=columns, rows=allRooms, row_key="id")


def deleteRoom():
    with ui.card().classes("flex-1 p-4"):
        ui.label("Enter a Room Id to delete").classes("text-subtitle1")
        toDelete = ui.input("Room Id")

        def onSubmit() -> None:
            submitInp = [toDelete.value]
            if checkValidity(submitInp):
                dbDelete(toDelete.value, DBPath)
                roomTable.refresh()

        ui.button("Submit", on_click=lambda: onSubmit())


def addRoom():
    with ui.card().classes("flex-1 p-4"):
        ui.label("Enter a Details to add a Room").classes("text-subtitle1")
        roomName = ui.input("Room Name")
        capacity = ui.input("Capacity")

        def onSubmit() -> None:
            submitInp = [roomName.value, capacity.value]
            if checkValidity(submitInp):
                dbAdd(roomName.value, capacity.value, DBPath)
                roomTable.refresh()

        ui.button("Submit", on_click=lambda: onSubmit())


def changeCapacity():
    with ui.card().classes("flex-1 p-4"):
        ui.label("Enter a Room Id to change Capacity").classes("text-subtitle1")
        roomId = ui.input("Room ID")
        capacity = ui.input("New Capacity")

        def onSubmit() -> None:
            submitInp = [roomId.value, capacity.value]
            checkValidity(submitInp)
            if checkValidity(submitInp):
                dbUpdate(roomId.value, capacity.value, DBPath)
                roomTable.refresh()

        ui.button("Submit", on_click=lambda: onSubmit())
