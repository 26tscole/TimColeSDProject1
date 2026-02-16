import os
import requests
from pathlib import Path
from datetime import datetime


class Users():
    def __init__(self):
        self.__loadSecrets()
        self.api_address = os.environ.get('API_ADDRESS')
        if not self.api_address:
            raise Exception('API_ADDRESS is not set')
        self.login_email = os.environ.get('LOGIN_EMAIL')
        if not self.login_email:
            raise Exception('LOGIN_EMAIL is not set')
        self.login_password = os.environ.get('LOGIN_PASSWORD')
        if not self.login_password:
            raise Exception('LOGIN_PASSWORD is not set')
        accessToken = self.login()
        self.auth = {'Authorization': 'Bearer ' + accessToken}

    # Might be temporary but trouble with getting the secretFile Path
    def __getSecretPath(self):
        current = Path(__file__).resolve()
        for parent in current.parents:
            secretFile = parent / "secret.txt"
            if secretFile.exists():
                return secretFile
        return None

    # loads secrets from file for running on machine
    def __loadSecrets(self):
        secretPath = self.__getSecretPath()
        if secretPath and os.path.exists(secretPath):
            with open(secretPath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value

    # Default method is GET
    def __makeRequest(self, url="", method='GET', data=None, isLogin=False):
        try:
            if isLogin:
                response = requests.post(url, json=data)
            elif method == 'GET':
                response = requests.get(url, headers=self.auth)
            elif method == 'POST':
                response = requests.post(url, headers=self.auth, json=data)
            elif method == 'DELETE':
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
        credentials = {
            "email": self.login_email,
            "password": self.login_password
        }
        response = self.__makeRequest(url=url, data=credentials, isLogin=True)
        if response:
            return response['token']['access']
        return False

    # Checks for available rooms can be used with startTime and endTime
    def getAvailableMeetings(self, startTime=None, endTime=None):
        url = self.api_address + "/api/v1/meeting-rooms/available/"
        if startTime or endTime:
            response = self.__makeRequest(url)
            return response
        else:
            params = {
                "start_time": startTime,
                "end_time": endTime
            }
            response = self.__makeRequest(url, data=params)
            return response

    # books meeting will return the response or False if room isnt available
    def bookMeeting(self, roomId: int, startTime, endTime, numPeople=2):
        url = self.api_address + f"/api/v1/meeting-rooms/{roomId}/book/"
        params = {
            "start_time":  startTime,
            "end_time": endTime,
            "no_of_persons": numPeople,
        }
        response = requests.post(url, json=params, headers=self.auth)
        if response:
            bookId = (self.getBookingByStartTime(startTime))['id']
            print("Successfully Booked Room: ", bookId)
            return bookId
        else:
            print("Room Could Not Be Booked")
            return False

    # returns bookings your account has made
    def getBookings(self):
        url = self.api_address + "/api/v1/meeting-rooms/my-bookings/"
        response = self.__makeRequest(url)
        return response

    # Allows you to delete bookings your account has made returns False if it doesnt work
    def deleteBooking(self, bookId: int):
        url = self.api_address + f"/api/v1/meeting-rooms/{bookId}/cancel-booking/"
        response = self.__makeRequest(url, method='DELETE')
        if response:
            print('Successfully removed booking with id:', bookId)
            return response
        else:
            print('No Booking With Id:', bookId)
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
            bookingTime = datetime.strptime(booking['start_time'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S")
            if bookingTime == startTime:
                print(booking)
                return booking
        return False
