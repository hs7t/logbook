import typer
from rich.console import Console
from pathlib import Path
from typing_extensions import Annotated
from typing import List, Tuple, Optional

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
def write(streak: str):
    console.print("I should print something!")

@app.command()
def read(
    tags: Annotated[Optional[List[str]], typer.Option(
        "-t", "--tag", help="A tag to look for in logs"
    )] = None,
):  
    console.print(tags)

@app.command()
def config():
    console.print("This should do something")

if __name__ == "__main__":
    app()