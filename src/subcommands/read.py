from enum import Enum
import typer

from rich.console import Console
from rich.table import Table
from rich import box

from interfaces.db import fetchLogs, findLogs, fetchTagDefinitions
import utilities.timekeeping as tk
import utilities.misc as misc
from typing_extensions import Annotated
from typing import List

from rich.progress import BarColumn, Progress, TextColumn

console = Console()
app = typer.Typer(help="Read your logbook.")

class LogSortingOption(str, Enum):
    # Sorting option -> table headers
    time = "timestamp"
    tag = "tag"
    text = "text"

    def __str__(self):
        return self.value
    
@app.command()
def logs(
    amount: int = typer.Argument(10, help="The amount of logs to show"),
    tags: Annotated[List[str]|None, typer.Option("-t", "--tag", help="A tag for your log")] = None,
    sortingOption: Annotated[LogSortingOption, typer.Option("-s", "--sort", help="How to sort logs")] = LogSortingOption.time,
    descending: Annotated[bool, typer.Option("-d/-a", "--descending/--ascending", help="Whether to order logs in descending order")] = True 
):
    """Read logs in your logbook."""
    with Progress(
        TextColumn("{task.description} [progress.percentage]"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total} items ({task.percentage:>3.0f}%)"),
        transient=True
    ) as progress:
        logs = []
        if tags is not None:
            task_reading = progress.add_task("Finding your logs...", total=len(tags))
            for tag in tags:
                logs.extend(findLogs(tag=tag))
                progress.advance(task_reading)
        else:
            task_reading = progress.add_task("Finding your logs...", total=1)
            logs = fetchLogs()
            progress.advance(task_reading)

        outputLogs = sorted(logs, key=lambda log: log[sortingOption], reverse=descending)
        outputLogs = outputLogs[:amount]

        table = Table(box=box.ROUNDED)

        table.add_column("Time (YYYY-MM-DD)", justify="center", no_wrap=True)
        table.add_column("Text", justify="center", style="bright_green", no_wrap=False)
        table.add_column("Tag", justify="center")
        # TODO: add 'state' column

        task_processing = progress.add_task("Making a neat table...", total=len(outputLogs))
        for log in outputLogs:
            datetime_local = tk.convertToTimeZone(tk.makeDatetime(log['timestamp']), tk.getLocalTimeZone())
            time_local = tk.makeTimeString(datetime_local, format="%Y-%m-%d, %H:%M:%S")
            table.add_row(time_local, f'"{log["body"]}"', log["tag"])
            progress.advance(task_processing)
    
    console.print(table)

@app.command()
def tags():
    """Read tags in your logbook."""
    tagDefs = fetchTagDefinitions()

    tagNames = [definition['name'] for definition in tagDefs]
    tagNames.sort()

    table = Table(box=box.ROUNDED)

    table.add_column("Tag", justify="center", style="bright_green")
    table.add_column("Last logged (Y-M-D)")
    table.add_column("State")

    for tagName in tagNames:
        matches = findLogs(tag=tagName)
        loggedTimes = [tk.makeDatetime(log['timestamp']) for log in matches]
        loggedTimes.sort(reverse=True)

        lastTimeString = "-"
        if loggedTimes:
            lastTimeString = tk.makeTimeString(tk.convertToTimeZone(loggedTimes[0], tk.getLocalTimeZone()), "%Y-%m-%d")
        
        state = misc.calculateState(matches)
        if state == 0:
            stateString = "-"
        else:
            stateString = str(state)

        table.add_row(tagName, lastTimeString, stateString)
    
    console.print(table)