from interfaces.db import resetAppFolder
import subcommands.subcommands.config.tag
from enum import Enum

import typer
from rich.console import Console

console = Console()

app = typer.Typer(help="Configure your logbook and other data.")

class DataAction(str, Enum):
    delete = "delete"

@app.command()
def data(
    action: DataAction = typer.Argument(help="An action to take (reset)"), 
):
    """
    Manage your app data.
    """
    if action == DataAction.delete:
        if typer.confirm("This will reset everything in your data folder, including your preferences and logbook. Are you sure?", default=False):
            resetAppFolder()
            console.print("Reset your logbook data folder.")

app.add_typer(subcommands.subcommands.config.tag.app, name="tag")