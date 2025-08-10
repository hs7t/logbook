import subcommands.subcommands.config.tag, subcommands.subcommands.config.delete
import typer
from rich.console import Console

console = Console()

app = typer.Typer(help="Configure your logbook and other data.")


app.add_typer(subcommands.subcommands.config.tag.app, name="tag")
app.add_typer(subcommands.subcommands.config.delete.app, name="data")