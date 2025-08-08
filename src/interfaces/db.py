import sqlite3
import dataset
import os
from pathlib import Path
from typing import Any

def makeAppFolder(path=(Path.home() / '.logbook')):
    appFolder = path.resolve()
    os.makedirs(appFolder, exist_ok=True)
    return appFolder

def pathToString(path):
    return path.absolute().as_posix()

appFolder = makeAppFolder()
db = dataset.connect(f'sqlite:///{appFolder}/logbook.db')

tags = db['tags']
logs = db['logs']

def createTag(name, kind = 'static', cadence = None):
    """
    Creates a tag reference.
        tag_name (str)
    """

    props: dict[str, Any] = dict( # typedef because pylance complains otherwise
        name = name,
        kind = kind
    )
    if kind == 'stateful':
        props['state'] = 0
    if cadence != None:
        props['cadence'] = cadence

    tags.insert(props) # pyright: ignore[reportOptionalMemberAccess]

def writeLog(body: str, timestamp: str|None = None, tag: str|None = None):
    """
    Writes a log to the database.
        body: text (str)
        timestamp: iso 8601 formatted timestamp (str)
        tag: tag in db['tags']
    """
    logs.insert(dict( # pyright: ignore[reportOptionalMemberAccess]
        body=body,
        tag=tag,
        timestamp=timestamp,
    ))

def fetchLogs():
    return logs.all() # pyright: ignore[reportOptionalMemberAccess]

def fetchLogsObject():
    return logs

def deleteLogs(query: dict):
    logs.delete(dict) # pyright: ignore[reportOptionalMemberAccess]

def deleteTag(tag):
    tags.delete(name = tag) # pyright: ignore[reportOptionalMemberAccess]