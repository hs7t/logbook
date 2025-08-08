from interfaces.db import createTag, deleteTag, fetchLogsObject
from typing_extensions import Annotated

import typer
from rich.console import Console

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
            if typer.confirm("This will update all logs related this tag. Are you sure?", default=True) is True:
                if typer.confirm("Would you like to change them to use a different tag?", default=True) is True:
                    newTag = typer.prompt("Please input another tag to use")
                    logsObject.update((tag = tag_name, tag = newTag))
                else:
                    if typer.confirm("All logs related to this tag will be deleted. Are you sure?", default=False) is False:
                        logsObject.delete(tag = tag_name)

            console.print("Deleted the tag tagName") # deleteTag(tag_name)
        else:
            if typer.confirm("Are you sure you'd like to delete this tag?", default=True) is True:
                console.print("Deleted the tag tagName") # deleteTag(tag_name)
