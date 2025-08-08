from interfaces.db import createTag
from typing_extensions import Annotated

import typer
from rich.console import Console

app = typer.Typer()

@app.command()
def tag(
    name: str = typer.Argument(help="A tag name"), 
):
    createTag(name, 'static')