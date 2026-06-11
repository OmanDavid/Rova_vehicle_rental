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

def prompt_int(label):
    """
    Prompt the user for an integer value, re-prompting on invalid input.

    Args:
        label (str): The prompt label.

    Returns:
        int: The validated integer value.
    """
    while True:
        value = input(f"{label}: ").strip()
        try:
            return int(value)
        except ValueError:
            console.print("[yellow]Please enter a whole number.[/yellow]")


def prompt_date(label):
    """
    Prompt the user for a date in YYYY-MM-DD format.

    Args:
        label (str): The prompt label.

    Returns:
        str: A valid date string in YYYY-MM-DD format.
    """
    while True:
        value = input(f"{label} (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(value, DATE_FORMAT)
            return value
        except ValueError:
            console.print("[yellow]Invalid date. Use YYYY-MM-DD format (e.g. 2025-08-01).[/yellow]")

def prompt_choice(label, valid_choices):
    """
    Prompt the user to pick from a list of valid choices.

    Args:
        label (str): The prompt label.
        valid_choices (list): List of acceptable string values.

    Returns:
        str: The validated choice in lowercase.
    """
    choices_str = ", ".join(valid_choices)
    while True:
        value = input(f"{label} ({choices_str}): ").strip().lower()
        if value in valid_choices:
            return value
        console.print(f"[yellow]Choose from: {choices_str}[/yellow]")
