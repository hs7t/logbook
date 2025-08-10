from rich.prompt import Confirm, Prompt
from rich.console import Console
from enum import Enum

console = Console()

class NotificationStyle(str, Enum):
    neutral = "blue"
    waffle = "grey54"
    warn = "bold yellow"
    assure = "green"
    hint = "yellow"

    def __str__(self):
        return self.value


def prompt(text, default=None, fade=True):
    if fade == True:
        style = NotificationStyle.waffle
        text = f"[{style}]{text}[{style}]"
    response = Prompt.ask(text, default=default)
    return response

def confirm(text, default=False, fade = False):
    if fade == True:
        style = NotificationStyle.waffle
        text = f"[{style}]{text}[{style}]"
    response = Confirm.ask(text, default=default)
    return response

def notify(text, style: NotificationStyle|str|None = NotificationStyle.neutral):
    if style == NotificationStyle.hint:
        text = f"💡 {text}"

    if style:
        console.print(f"[{style}]{text}[/{style}]")
    else:
        console.print(text)