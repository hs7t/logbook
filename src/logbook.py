import subcommands.config
import typer
from rich.console import Console

from interfaces.db import writeLog, readLogs
from utilities.timekeeping import getCurrentUTC, isoTimeString
from typing_extensions import Annotated
from typing import List


console = Console()

app = typer.Typer(add_completion = False)

@app.callback(invoke_without_command = True)
def main(ctx: typer.Context):
    # Do not run when invoked with subcommands
    if ctx.invoked_subcommand is not None:
        return
    console.print("[blue]logbook[/blue]")
    console.print("Try running --help!")

@app.command()
def write(
    body: str = typer.Argument(help="Text for your log"),
    tag: Annotated[str|None, typer.Option("-t", "--tag", help="A tag for your log")] = None,
):
    now = isoTimeString(getCurrentUTC())
    if tag is not None:
        writeLog(body, timestamp=now, tag=tag)
    else:
        writeLog(body, timestamp=now)

@app.command()
def read(
    amount: int = typer.Argument(10, help="The amount of logs to show"),
    tag: Annotated[List[str]|None, typer.Option("-t", "--tag", help="A tag for your log")] = None,
):
    for log in readLogs():
        console.print(log)
    

app.add_typer(subcommands.config.app, name="config")

if __name__ == "__main__":
    app()