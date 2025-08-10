import subcommands.config
import typer

from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich import box

from interfaces.db import fetchLogs, findLogs, fetchTagDefinitions
import utilities.timekeeping as tk
from typing_extensions import Annotated
from typing import List

console = Console()
app = typer.Typer(help="Configure your logbook and other data.")

@app.command()
def logs(
    amount: int = typer.Argument(10, help="The amount of logs to show"),
    tags: Annotated[List[str]|None, typer.Option("-t", "--tag", help="A tag for your log")] = None,
    descending: Annotated[bool, typer.Option("-d/-a", "--descending/ascending", help="Whether to order logs in descending order")] = True 
):
    logs = []
    if tags is not None:
        for tag in tags:
            logs.extend(findLogs(tag=tag))
    else:
        logs = fetchLogs()

    outputLogs = sorted(logs, key=lambda log: log["timestamp"], reverse=descending)
    outputLogs = outputLogs[:amount]

    table = Table(box=box.ROUNDED)

    table.add_column("Time (YYYY-MM-DD)", justify="center", no_wrap=True)
    table.add_column("Text", justify="center", style="bright_green", no_wrap=False)
    table.add_column("Tag", justify="center")

    for log in outputLogs:
        datetime_local = tk.convertToTimeZone(tk.makeDatetime(log['timestamp']), tk.getLocalTimeZone())
        time_local = tk.makeTimeString(datetime_local, format="%Y-%m-%d, %H:%M:%S")
        table.add_row(time_local, f'"{log['body']}"', log['tag'])
    
    console.print(table)

@app.command()
def tags():
    tagDefs = fetchTagDefinitions()

    tagNames = [definition['name'] for definition in tagDefs]
    tagNames.sort()

    table = Table(box=box.ROUNDED)

    table.add_column("Tag", justify="center", style="bright_green")
    table.add_column("Last logged (Y-M-D)")

    for tagName in tagNames:
        matches = findLogs(tag=tagName)
        loggedTimes = [tk.makeDatetime(log['timestamp']) for log in matches]
        loggedTimes.sort(reverse=True)

        lastTimeString = "-"
        if loggedTimes[0]:
            lastTimeString = tk.makeTimeString(tk.convertToTimeZone(loggedTimes[0], tk.getLocalTimeZone()), "%Y-%m-%d")
        
        table.add_row(tagName, lastTimeString)
    
    console.print(table)