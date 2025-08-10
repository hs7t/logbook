import sqlite3, dataset
from enum import Enum
import os, shutil
from pathlib import Path
from typing import Any

def loadAppFolder(path=(Path.home() / '.logbook')):
    appFolder = path.resolve()
    os.makedirs(appFolder, exist_ok=True)
    return appFolder

def resetAppFolder(path=(Path.home() / '.logbook')):
    appFolder = path.resolve()
    if os.path.exists(appFolder):
        shutil.rmtree(appFolder)
    loadAppFolder(path)

def pathToString(path):
    return path.absolute().as_posix()

appFolder = loadAppFolder()
db = dataset.connect(f'sqlite:///{appFolder}/logbook.db')

tags = db['tags']
logs = db['logs']

# Tags
class TagKind(str, Enum):
    static = "static"
    stateful = "stateful"
    cadenced = "cadenced"

def createTagDefinition(name, kind: TagKind = TagKind.static, cadence = None):
    """
    Creates a tag reference.
        name: the name for the tag (str)
    """

    props: dict[str, Any] = dict( # typedef because pylance complains otherwise
        name = name,
        kind = kind
    )
    if kind == TagKind.stateful:
        props['state'] = 0
    if kind == TagKind.stateful and cadence != None:
        props['cadence'] = cadence

    tags.insert(props) # pyright: ignore[reportOptionalMemberAccess]

def deleteTagDefinition(tag):
    tags.delete(name = tag) # pyright: ignore[reportOptionalMemberAccess]

def findTagDefinitions(**kwargs):
    return [match for match in tags.find(**kwargs)] # pyright: ignore[reportOptionalMemberAccess]

def fetchTagDefinitions():
    return tags.all() # pyright: ignore[reportOptionalMemberAccess]

# Logs

def writeLog(body: str, timestamp: str|None = None, tag: str|None = None, stateModifier: int|None = None):
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

def deleteAllLogs():
    logs.delete() # pyright: ignore[reportOptionalMemberAccess]

def deleteLogsByTag(tag):
    logs.delete(tag=tag) # pyright: ignore[reportOptionalMemberAccess]

def fetchLogs():
    return logs.all() # pyright: ignore[reportOptionalMemberAccess]

def fetchLogsObject():
    return logs

def findLogs(*args, **kwargs):
    return [match for match in logs.find(*args, **kwargs)] # pyright: ignore[reportOptionalMemberAccess]

def changeLogTags(old_tag: str, new_tag: str):
    """
    Changes the tag attribute to a new_tag for all logs using a certain old_tag
    """

    # I know this is bad code but it's the best workaround :(
    updateData = dict(tag = old_tag, _tmp = old_tag)
    logs.update(updateData, ['tag']) # pyright: ignore[reportOptionalMemberAccess]

    updateData = dict(_tmp = old_tag, tag = new_tag)
    logs.update(updateData, ['_tmp']) # pyright: ignore[reportOptionalMemberAccess]
