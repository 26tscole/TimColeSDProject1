from datetime import datetime
from langchain.tools import tool


# Global variable to store the Users instance
_users_instance = None

def setUsersInstance(users_obj):
    """Set the Users instance for tools to use"""
    global _users_instance
    _users_instance = users_obj

@tool
def getCurrentDatetime() -> str:
    """Get the current date and time in the format %Y-%m-%d %H:%M:%S"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def getAvailableMeetings(start_time: str = None, end_time: str = None) -> list:
    """Get available meeting rooms. Optionally filter by start_time and end_time in format YYYY-MM-DD HH:MM"""
    if _users_instance is None:
        return ["Error: Users instance not initialized"]
    return _users_instance.getAvailableMeetings(start_time, end_time)

@tool
def getBookings() -> list:
    """Get all current bookings for the logged-in user"""
    if _users_instance is None:
        return ["Error: Users instance not initialized"]
    return _users_instance.getBookings()
