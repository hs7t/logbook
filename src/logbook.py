import subcommands.config
import typer

from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich import box

from interfaces.db import writeLog, fetchLogs, deleteAllLogs, deleteLogsByTag
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
def delete(
    tags: Annotated[List[str]|None, typer.Option("-t", "--tag", help="A tag to delete items by")] = None,
):
    """Deletes logs in your logbook."""
    if not tags: # IMPORTANT; update when new filter type
        if Confirm.ask("[red]It looks like you're trying to delete every single log in your logbook.[/red] Are you sure?", default=False):
            deleteAllLogs()
    elif tags:
        for tag in tags:
            deleteLogsByTag(tag)
        console.print("Done!")

@app.command()
def read(
    amount: int = typer.Argument(10, help="The amount of logs to show"),
    tag: Annotated[List[str]|None, typer.Option("-t", "--tag", help="A tag for your log")] = None,
):
    logs = fetchLogs()
    table = Table(box=box.ROUNDED)

    table.add_column("Timestamp", justify="center", style="bright_yellow", no_wrap=True)
    table.add_column("Text", style="bright_green", no_wrap=False)
    table.add_column("Tag", justify="center")

    for log in logs:
        table.add_row(log['timestamp'], f'"{log['body']}"', log['tag'])
    
    console.print(table)
    

app.add_typer(subcommands.config.app, name="config")

if __name__ == "__main__":
    app()