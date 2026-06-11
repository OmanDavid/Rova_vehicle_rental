"""
decorators.py — Reusable decorators for authentication and role-based access.

Usage:
    @require_login
    def some_action(current_user):
        ...

    @admin_only
    def admin_action(current_user):
        ...
"""

from functools import wraps
from rich.console import Console # type: ignore

console = Console()

# Holds the currently logged-in user for this session
_current_user = None


def set_current_user(user):
    """Set the active session user."""
    global _current_user
    _current_user = user

def get_current_user():
    """Get the active session user."""
    return _current_user

def logout():
    """Clear the session user."""
    global _current_user
    _current_user = None

def require_login(func):
    """
    Decorator — blocks access if no user is logged in.
    Passes the current user as the first argument to the wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _current_user is None:
            console.print("[red]✗ You must be logged in to do that.[/red]")
            return
        return func(_current_user, *args, **kwargs)
    return wrapper

def admin_only(func):
    """
    Decorator — blocks access if the current user is not an admin.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _current_user is None:
            console.print("[red]✗ You must be logged in to do that.[/red]")
            return
        if not _current_user.is_admin():
            console.print("[red]✗ Admin access required.[/red]")
            return
        return func(_current_user, *args, **kwargs)
    return wrapper

def log_action(func):
    """
    Decorator — logs the name of every function call to the console.
    Useful for debugging and audit trails.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = _current_user.username if _current_user else "guest"
        console.print(f"[dim]› {user} called {func.__name__}[/dim]")
        return func(*args, **kwargs)
    return wrapper





