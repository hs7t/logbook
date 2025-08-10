from interfaces.db import resetAppFolder
import subcommands.subcommands.config.tag

import typer
import utilities.display as display
from rich.console import Console

console = Console()

app = typer.Typer(help="Manage your app data.")


app.add_typer(subcommands.subcommands.config.tag.app, name="tag")

@app.command()
def delete():
    """
    Delete your app data.
    """
    display.notify("This will reset everything in your data folder, including your preferences and logbook.", display.NotificationStyle.warn)
    if display.confirm("Are you sure?", default=False):
        resetAppFolder()
        display.notify("Reset your logbook data folder.", display.NotificationStyle.assure)
