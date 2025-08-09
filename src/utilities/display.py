from rich.prompt import Confirm, Prompt

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