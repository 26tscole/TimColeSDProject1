from nicegui import ui
from src.meetIngActions.users import Users


def roomTable():
    user = Users()
    allRooms = user.getAvailableMeetings()
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'room_name', 'label': 'Room Name', 'field': 'room_name'},
        {'name': 'capacity', 'label': 'Capacity', 'field': 'capacity'},
    ]
    with ui.card().classes('w-full p-4'):
        ui.label('All Available Rooms').classes('text-subtitle1')
        ui.table(columns=columns, rows=allRooms, row_key='id')
