import os
from pathlib import Path

def openPath(path):
    os.makedirs(path.parent, exist_ok=True)
    return open(path)