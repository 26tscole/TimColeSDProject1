from nicegui import ui
from src.meetIngActions.users import Users


def submitText(items: list[str]) -> None:
    isMissing = any(item == '' for item in items)
    print(items)
    if isMissing:
        ui.notify('Cannot Submit: Missing Fields')
    else:
        ui.notify(f'You entered: {items}')

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

def deleteRoom():
    with ui.card().classes('w-full p-4'):
        ui.label('Enter a Room Id to delete').classes('text-subtitle1')
        toDelete = ui.input('Room Id')

        def onSubmit() -> None:
            submitInp = [toDelete.value]
            submitText(submitInp)

        ui.button('Submit', on_click= lambda: onSubmit())

def addRoom():
    with ui.card().classes('w-full p-4'):
        ui.label('Enter a Details to add a Room').classes('text-subtitle1')
        roomName = ui.input('Room Name')
        capacity = ui.input('Capacity')

        def onSubmit() -> None:
            submitInp = [roomName.value, capacity.value]
            submitText(submitInp)

        ui.button('Submit', on_click=lambda: onSubmit())

def changeCapacity():
    with ui.card().classes('w-full p-4'):
        ui.label('Enter a Room Id to change Capacity').classes('text-subtitle1')
        roomId = ui.input('Room ID')
        capacity = ui.input('New Capacity')

        def onSubmit() -> None:
            submitInp = [roomId.value, capacity.value]
            submitText(submitInp)

        ui.button('Submit', on_click=lambda: onSubmit())