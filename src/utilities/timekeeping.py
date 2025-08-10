from datetime import datetime
from zoneinfo import ZoneInfo
from tzlocal import get_localzone 

def getCurrentUTC():
    return datetime.now(tz=ZoneInfo("UTC"))

def getLocalTimeZone():
    return get_localzone()

def convertToTimeZone(datetime: datetime, timezone: ZoneInfo):
    return datetime.astimezone(timezone)

def makeTimeString(datetime: datetime, format: str):
    """Makes a string from a datetime using a format"""
    return datetime.strftime(format)

def makeISOTimeString(UTCDatetime): 
    """Turns an UTC datetime into an ISO time string"""
    return makeTimeString(UTCDatetime, "%Y-%m-%dT%H:%M:%SZ")

def makeDatetime(ISOTimeString):
    """Turns an ISO timestring into a UTC datetime"""
    return datetime.fromisoformat(ISOTimeString)