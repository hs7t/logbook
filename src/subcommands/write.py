import typer
from typing_extensions import Annotated

from interfaces.db import writeLog
from utilities.timekeeping import getCurrentUTC, isoTimeString

app = typer.Typer()

@app.command()
def main(
    body: str = typer.Argument(help="Text for your log"),
    tag: Annotated[str|None, typer.Option(None, "-t", "--tag", help="A tag for your log")] = None,
):
    now = isoTimeString(getCurrentUTC())
    writeLog(body, timestamp=now, tag=tag)