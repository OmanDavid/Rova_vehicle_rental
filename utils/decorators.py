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