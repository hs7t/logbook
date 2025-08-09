from interfaces.db import createTag, changeLogTags, deleteLogsByTag, fetchLogsObject
from interfaces.db import resetAppFolder

from typing_extensions import Annotated

import typer
from rich.console import Console
from rich import print

console = Console()

app = typer.Typer()

@app.command()
def tag(
    action: str = typer.Argument(help="An action to take (create/delete)"), 
    tag_name: str = typer.Argument(help="A tag name"), 
):
    if action == 'create':
        createTag(tag_name, 'static')

    if action == 'delete':
        logsObject = fetchLogsObject()
        matchingEntries = [entry for entry in logsObject.find(tag=tag_name)] # pyright: ignore[reportOptionalMemberAccess]

        if len(matchingEntries) != 0:
            if typer.confirm("This will update all logs related this tag. Are you sure?", default=True):
                if typer.confirm("Would you like to change them to use a different tag?", default=True):
                    new_tag = typer.prompt("Please input another tag to use")
                    changeLogTags(new_tag=new_tag, old_tag=tag_name)
                else:
                    if typer.confirm("All logs related to this tag will be deleted. Are you sure?", default=False):
                        deleteLogsByTag(tag_name)

            console.print("Deleted the tag tagName") # deleteTag(tag_name)
        else:
            if typer.confirm("Are you sure you'd like to delete this tag?", default=True) is True:
                console.print("Deleted the tag tagName") # deleteTag(tag_name)

@app.command()
def data(
    action: str = typer.Argument(help="An action to take (reset)"), 
):
    if action == 'reset':
        if typer.confirm("This will reset everything in your data folder, including your preferences and logbook. Are you sure?", default=False):
            resetAppFolder()
            console.print("Reset your logbook data folder.")