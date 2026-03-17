from nicegui import ui
from layout import roomTable
from src.meetIngActions.users import Users

@ui.page('/')
def page():
    ui.page_title('Room Bookings')
    roomTable()

ui.run()

if __name__ == "__main__":
    user = Users()
    allMeetings = user.getAvailableMeetings()
    print(allMeetings)

