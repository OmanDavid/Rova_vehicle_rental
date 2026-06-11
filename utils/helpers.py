from datetime import datetime
from rich.console import Console

console = Console()
DATE_FORMAT = "%Y-%m-%d"


def prompt(label, required=True):
    """
    Prompt the user for input.

    Args:
        label (str): The prompt label shown to the user.
        required (bool): If True, re-prompts until non-empty input is given.

    Returns:
        str: The user's input stripped of whitespace.
    """
    while True:
        value = input(f"{label}: ").strip()
        if value or not required:
            return value
        console.print("[yellow]This field is required.[/yellow]")

