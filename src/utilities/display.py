from rich.prompt import Confirm, Prompt
from rich.console import Console
from enum import Enum

console = Console()

def prompt(text, default=None, fade=False):
    if fade is True:
        text = f"[grey54]{text}[/grey54]"

    response = Prompt.ask(text, default=default)
    return response

def confirm(text, default=False, fade = False):
    if fade is True:
        text = f"[grey54]{text}[/grey54]"

    response = Confirm.ask(text, default=default)
    return response

class NotificationStyle(str, Enum):
    neutral = "blue",
    waffle = "grey54",
    warn = "bold yellow",
    assure = "green"

def notify(text, style: NotificationStyle|str = NotificationStyle.neutral):
    console.print(f"[{style}]{text}[/{style}]")