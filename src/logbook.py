import subcommands.config, subcommands.write
import typer

from rich.console import Console
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

app.add_typer(subcommands.config.app, name="config")
app.add_typer(subcommands.write.app, name="config")

if __name__ == "__main__":
    app()