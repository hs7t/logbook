from datetime import datetime
from zoneinfo import ZoneInfo

def getCurrentUTC():
    return datetime.now(tz=ZoneInfo("UTC"))

def isoTimeString(UTCTimeString): 
    """Turns an UTC datetime into an UTC time string"""
    return UTCTimeString.strftime("%Y-%m-%dT%H:%M:%SZ")