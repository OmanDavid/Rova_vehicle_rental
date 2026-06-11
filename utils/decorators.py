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
from rich.console import Console

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