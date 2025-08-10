import subcommands.config, subcommands.read
from subcommands.config import TagAction
import typer

from interfaces.db import writeLog, deleteAllLogs, deleteLogsByTag, findTagDefinitions, TagKind
import utilities.display as display
from utilities.display import NotificationStyle
import utilities.timekeeping as tk
from typing_extensions import Annotated
from typing import List

app = typer.Typer(add_completion = False)

@app.callback(invoke_without_command = True)
def main(ctx: typer.Context):
    # Do not run when invoked with subcommands
    if ctx.invoked_subcommand is not None:
        return
    display.notify("logbook", NotificationStyle.waffle)
    display.notify("Try running --help!", NotificationStyle.hint)

@app.command()
def write(
    body: str = typer.Argument(help="Text for your log"),
    modifier: Annotated[int|None, typer.Argument(help="A modifier for a tag state")] = None,
    tag: Annotated[str|None, typer.Option("-t", "--tag", help="A tag for your log")] = None,
):
    """Write logs to your logbook."""
    now = tk.makeISOTimeString(tk.getCurrentUTC())

    if tag is not None:
        if len(findTagDefinitions(name=tag)) == 0:
            display.notify("It looks like that tag doesn't exist.")
            if display.confirm(f"Would you like to create a new tag named {tag}?", default=True) is True:
                subcommands.config.tag(TagAction.create, tag)
                display.notify(f"Created a new tag named {tag}.", NotificationStyle.assure)
            else:
                raise typer.Exit()
        if findTagDefinitions(name='tag', kind=TagKind.stateful.value):
            writeLog(body, timestamp=now, tag=tag, stateModifier=modifier)
        else:
            writeLog(body, timestamp=now, tag=tag)
    else:
        writeLog(body, timestamp=now)



    display.notify("Wrote your log!", NotificationStyle.assure)

@app.command()
def delete(
    tags: Annotated[List[str]|None, typer.Option("-t", "--tag", help="A tag to delete items by")] = None,
):
    """Delete logs in your logbook."""
    if not tags: # IMPORTANT; update when new filter type
        display.notify("It looks like you're trying to delete every single log in your logbook.", NotificationStyle.warn) 
        if display.confirm("Are you sure?", default=False):
            deleteAllLogs()
            display.notify("Done! Deleted all logs.", NotificationStyle.assure)
    elif tags:
        for tag in tags:
            deleteLogsByTag(tag)
        display.notify(f"Done! Deleted all logs with the tag{'s' if len(tags) > 1 else ''} you selected.", NotificationStyle.assure)   

app.add_typer(subcommands.config.app, name="config")
app.add_typer(subcommands.read.app, name="read")

if __name__ == "__main__":
    app()