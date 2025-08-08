import sqlite3
import dataset
import os
from pathlib import Path

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

def createTag(tag_name):
    tags.insert(dict(id=tag_name))