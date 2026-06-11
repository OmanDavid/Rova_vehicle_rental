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

def prompt_float(label):
    """
    Prompt the user for a float value, re-prompting on invalid input.

    Args:
        label (str): The prompt label.

    Returns:
        float: The validated float value.
    """
    while True:
        value = input(f"{label}: ").strip()
        try:
            return float(value)
        except ValueError:
            console.print("[yellow]Please enter a valid number.[/yellow]")


