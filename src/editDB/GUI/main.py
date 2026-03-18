from nicegui import ui
from layout import roomTable, deleteRoom, addRoom, changeCapacity
from src.meetIngActions.users import Users

@ui.page('/')
def page():
    ui.page_title('Room Bookings')
    roomTable()
    deleteRoom()
    addRoom()
    changeCapacity()

ui.run()

if __name__ == "__main__":
    user = Users()
    allMeetings = user.getAvailableMeetings()
    print(allMeetings)

