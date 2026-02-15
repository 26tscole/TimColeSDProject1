import os
import requests


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
        accessToken = self.__login()
        self.auth = {'Authorization': 'Bearer ' + accessToken}

    def __loadSecrets(self):
        filepath = os.path.join('..', '..', 'secret.txt')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
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
    def __login(self):
        url = self.api_address + "/api/v1/member/login/"
        credentials = {
            "email": self.login_email,
            "password": self.login_password
        }
        response = self.__makeRequest(url=url, data=credentials, isLogin=True)
        if response:
            return response['token']['access']
        return False

    def getAvailableMeetings(self):
        url = self.api_address + "/api/v1/meeting-rooms/available/"
        response = self.__makeRequest(url)
        return response

    def bookMeeting(self, roomId: int, startTime, endTime, numPeople=2):
        url = self.api_address + f"/api/v1/meeting-rooms/{roomId}/book/"
        params = {
            "start_time":  startTime,
            "end_time": endTime,
            "no_of_persons": numPeople,
        }
        response = requests.post(url, json=params, headers=self.auth)
        if response:
            print("Successfully Booked Room: ", response)
            return response
        else:
            print("Room Could Not Be Booked")
            return False

    def getBookings(self):
        url = self.api_address + "/api/v1/meeting-rooms/my-bookings/"
        response = self.__makeRequest(url)
        return response

    def deleteBooking(self, bookId: int):
        url = self.api_address + f"/api/v1/meeting-rooms/{bookId}/cancel-booking/"
        response = self.__makeRequest(url, method='DELETE')
        if response:
            print('Successfully removed booking with id:', bookId)
            return response
        else:
            print('No Booking With Id:', bookId)
            return False

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
