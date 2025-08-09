from interfaces.db import createTagDefinition, findTagDefinitions, deleteTagDefinition, findLogs, changeLogTags
from interfaces.db import resetAppFolder
import utilities.display as display
from typing_extensions import Annotated

import typer
from rich.console import Console

console = Console()

app = typer.Typer(help="Configure your logbook and other data.")

@app.command()
def tag(
    action: str = typer.Argument(help="An action to take (create/delete)"), 
    tag_name: str = typer.Argument(help="A tag name"), 
):
    """
    Configure tags.
    """
    if action == 'create':
        createTagDefinition(tag_name, 'static')

    if action == 'delete':
        if len(findTagDefinitions(name=tag_name)) == 0:
            console.print("[blue]It looks like that tag doesn't exist.[/blue]")
            raise typer.Exit()

        if len(findLogs(tag=tag_name)) != 0:
            if display.confirm("[bold red]This will update all logs related to this tag.[/bold red] Are you sure?", default=True) is False:
                raise typer.Exit()

            if display.confirm("Would you like to update related logs to use a different tag?", default=True):
                new_tag_exists = False
                while new_tag_exists is False:
                    new_tag = display.prompt("Please input another tag to use", fade=True) or ""
                    if len(findTagDefinitions(name=new_tag)) > 0 and new_tag != tag_name:
                        changeLogTags(new_tag=new_tag, old_tag=tag_name)
                        new_tag_exists = True
                    else:
                        console.print("[blue]It looks like that tag doesn't exist.[/blue]")
            else:
                if display.confirm("[bold red]All logs related to this tag will be deleted.[/bold red] Are you sure?", default=False) is False:
                    raise typer.Exit()
        else:
            if typer.confirm("[yellow]This tag will be deleted.[/yellow] Are you sure?", default=True) is False:
                raise typer.Exit()
        
        deleteTagDefinition(tag_name)
        console.print(f"Deleted the tag {tag_name}")

@app.command()
def data(
    action: str = typer.Argument(help="An action to take (reset)"), 
):
    """
    Manage your app data.
    """
    if action == 'reset':
        if typer.confirm("This will reset everything in your data folder, including your preferences and logbook. Are you sure?", default=False):
            resetAppFolder()
            console.print("Reset your logbook data folder.")