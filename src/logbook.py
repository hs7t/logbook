import subcommands.config, subcommands.read
import typer

from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich import box

from interfaces.db import writeLog, fetchLogs, findLogs, deleteAllLogs, deleteLogsByTag, findTagDefinitions
import utilities.display as display
import utilities.timekeeping as tk
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
    now = tk.makeISOTimeString(tk.getCurrentUTC())
    if tag is not None:
        if len(findTagDefinitions(name=tag)) == 0:
            if display.confirm("[blue] It looks like that tag doesn't exist. Would you like to create it?", default=True) is True:
                subcommands.config.tag('create', tag)
                console.print(f"Created a new tag [blue]{tag}[/blue]")
            else:
                raise typer.Exit()
        writeLog(body, timestamp=now, tag=tag)
        console.print("Wrote your log!")
    else:
        writeLog(body, timestamp=now)
        console.print("Wrote your log!")

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

app.add_typer(subcommands.config.app, name="config")
app.add_typer(subcommands.read.app, name="read")

if __name__ == "__main__":
    app()