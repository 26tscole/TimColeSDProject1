from users import Users
import os
import json


if __name__ == '__main__':
    currentUser = Users()
    while True:
        action = input("Choose an Action By Number:\n"
                       "1  --Check Available Meetings--\n"
                       "2  --Book a Meeting Room--\n"
                       "3  --Check Your Current Bookings--\n"
                       "4  --Delete a Booked Meeting--\n"
                       "\n"
                       "-----------------------------\n"
                       "q  --End Program--\n"
                       "-----------------------------\n")
        match action:
            case "1":
                response = currentUser.getAvailableMeetings()
                currentUser.printFormattedResponse(response)
            case "2":
                response = currentUser.getAvailableMeetings()
                currentUser.printFormattedResponse(response)
                canBook = False
                while not canBook:
                    print("Fill Out Needed Info To Book a Room: ")
                    print("(Make sure meeting is no longer than 15 Minutes)")
                    roomId = int(input("Pick Room Id from list: "))
                    startTime = input("Choose start time in (yyyy-mm-dd hh:mm AM) format: ")
                    endTime = input("Choose end time in (yyyy-mm-dd hh:mm AM) format: ")
                    canBook = currentUser.bookMeeting(roomId, startTime, endTime)

            case "3":
                response = currentUser.getBookings()
                currentUser.printFormattedResponse(response)
            case "4":
                response = currentUser.getBookings()
                currentUser.printFormattedResponse(response)
                idExists = False
                while not idExists:
                    deleteId = int(input("Choose a Booking By Id to Delete: "))
                    idExists = currentUser.deleteBooking(deleteId)
            case "e":
                print("No Current Action Running")
            case "q":
                print("Goodbye!")
                break
            case _:
                print("No Action Assigned to: ", action)