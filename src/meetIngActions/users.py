import os
import requests
from datetime import datetime
from src.setEnviron import loadSecrets


class Users:
    def __init__(self):
        """ "
        Initializes Users class which will allows for server connection and ability to call functions.

        """
        loadSecrets()
        self.api_address = os.environ.get("API_ADDRESS")
        if not self.api_address:
            raise Exception("API_ADDRESS is not set")
        self.login_email = os.environ.get("LOGIN_EMAIL")
        if not self.login_email:
            raise Exception("LOGIN_EMAIL is not set")
        self.login_password = os.environ.get("LOGIN_PASSWORD")
        if not self.login_password:
            raise Exception("LOGIN_PASSWORD is not set")
        accessToken = self.login()
        self.auth = {"Authorization": "Bearer " + accessToken}

    # Default method is GET
    def __makeRequest(self, url="", method="GET", data=None, isLogin=False):
        try:
            if isLogin:
                response = requests.post(url, json=data)
            elif method == "GET":
                response = requests.get(url, headers=self.auth)
            elif method == "POST":
                response = requests.post(url, headers=self.auth, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.auth)
            else:
                raise ValueError(f"Unsupported method: {method}")
            if not response:
                return False
            response.raise_for_status()
            if response.status_code == 204 or not response.text:
                return True
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        return None

    # logs user in and returns the jwt token
    def login(self):
        url = self.api_address + "/api/v1/member/login/"
        credentials = {"email": self.login_email, "password": self.login_password}
        response = self.__makeRequest(url=url, data=credentials, isLogin=True)
        if response:
            return response["token"]["access"]
        return False

    # Checks for available rooms can be used with startTime and endTime
    def getAvailableMeetings(self, startTime=None, endTime=None):
        """ "

        Args:
            startTime: String in format YYYY-MM-DD HH:MM used to find available meetings in between this and ending time
            endTime: String in format YYYY-MM-DD HH:MM used to find available meetings in between this and starting time

        Returns:
            A JSON object that has information about all the fetched booked meetings

        """
        url = self.api_address + "/api/v1/meeting-rooms/available/"
        if startTime or endTime:
            response = self.__makeRequest(url)
            return response
        else:
            params = {"start_time": startTime, "end_time": endTime}
            response = self.__makeRequest(url, data=params)
            return response

    # books meeting will return the response or False if room isn't available
    def bookMeeting(self, roomId: int, startTime, endTime, numPeople=2):
        url = self.api_address + f"/api/v1/meeting-rooms/{roomId}/book/"
        params = {
            "start_time": startTime,
            "end_time": endTime,
            "no_of_persons": numPeople,
        }
        response = self.__makeRequest(url, method="POST", data=params)
        if response:
            bookId = (self.getBookingByStartTime(startTime))["id"]
            print("Successfully Booked Room with Id: ", bookId)
            return bookId
        else:
            print("Room Could Not Be Booked")
            return False

    # returns bookings your account has made
    def getBookings(self):
        """ "

        Returns:
            A JSON object that has information about all the currently booked meetings

        """
        url = self.api_address + "/api/v1/meeting-rooms/my-bookings/"
        response = self.__makeRequest(url)
        return response

    # Allows you to delete bookings your account has made returns False if it doesn't work
    def deleteBooking(self, bookId: int):
        url = self.api_address + f"/api/v1/meeting-rooms/{bookId}/cancel-booking/"
        response = self.__makeRequest(url, method="DELETE")
        if response:
            print("Successfully removed booking with id:", bookId)
            return response
        else:
            print("No Booking With Id:", bookId)
            return False

    # just using this to make the main look good
    def printFormattedResponse(self, response):
        for firstObject in response:
            for key, value in firstObject.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for itemKey, itemValue in value.items():
                        print("\t", itemKey, ": ", itemValue)
                else:
                    print(f"{key}: {value}")
            print("-" * 50)

    # this function searches for the id of the meeting with the inputted date
    def getBookingByStartTime(self, startTime):
        startTime = datetime.strptime(startTime, "%Y-%m-%d %I:%M %p")
        for booking in self.getBookings():
            bookingTime = datetime.strptime(
                booking["start_time"].rstrip("Z"), "%Y-%m-%dT%H:%M:%S"
            )
            if bookingTime == startTime:
                return booking
        return False
