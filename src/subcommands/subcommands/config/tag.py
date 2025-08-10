from interfaces.db import createTagDefinition, findTagDefinitions, deleteTagDefinition, findLogs, changeLogTags, TagKind
import utilities.misc as misc
import utilities.display as display
from enum import Enum

import typer
from rich.console import Console

console = Console()

app = typer.Typer(help="Configure tags.")

class TagAction(str, Enum):
    create = "create"
    delete = "delete"
    update = "update"

@app.command()
def create(
    tag_name: str = typer.Argument(help="A name for the new tag"),
    tag_kind: TagKind = typer.Option(help="The tag's kind", default=TagKind.static), 
):
    """
    Create a new tag.
    """
    tagExists = misc.hasItems(findTagDefinitions(name=tag_name))

    if tagExists is True:
        console.print(f"That tag ({tag_name}) already exists.")
        raise typer.Exit()
    
    createTagDefinition(tag_name, tag_kind)
    console.print(f"Tag {tag_name} created!")


@app.command()
def delete(
    tag_name: str = typer.Argument(help="A tag name"), 
):
    """
    Delete a tag.
    """

    tag_exists = misc.hasItems(findTagDefinitions(name=tag_name))

    if tag_exists is False:
        display.notify("It looks like that tag doesn't exist.")
        raise typer.Exit()

    if misc.hasItems(findLogs(tag=tag_name)) is True:
        display.notify("This will update all logs related to this tag.", style=display.NotificationStyle.warn)
        if display.confirm("Are you sure?", default=True, fade=True) is False:
            raise typer.Exit()

        if display.confirm("Would you like to update related logs to use a different tag?", default=True):
            new_tag_exists = False
            while new_tag_exists is False:
                new_tag = display.prompt("Please input another tag to use") or ""
                if len(findTagDefinitions(name=new_tag)) > 0 and new_tag != tag_name:
                    changeLogTags(new_tag=new_tag, old_tag=tag_name)
                    new_tag_exists = True
                else:
                    display.notify("It looks like that tag doesn't exist.")
        elif display.confirm("Would you like to unlink this tag from all its related logs?"):
            changeLogTags(tag_name, None)
            display.notify("Unlinked all logs from this tag", display.NotificationStyle.assure)
        else:
            display.notify("All logs related to this tag will be deleted", display.NotificationStyle.warn)
            if display.confirm("Are you sure?") is False:
                raise typer.Exit()
    else:
        if display.confirm("[yellow]This tag will be deleted.[/yellow] Are you sure?", default=True) is False:
            raise typer.Exit()
    
    deleteTagDefinition(tag_name)
    console.print(f"Deleted the tag {tag_name}")

