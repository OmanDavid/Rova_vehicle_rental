"""
main.py — Rova CLI entry point.
Uses argparse subcommands for all actions.
Run python main.py --help to see all commands.
"""

import argparse
import sys
from rich.console import Console

from utils.auth import register, login, seed_admin
from utils.decorators import set_current_user
from lib.functions import (
    add_vehicle, list_vehicles, search_vehicle,
    add_customer, list_customers,
    create_booking, list_bookings, cancel_booking,
)

console = Console()


def authenticate():
    """Ask for login credentials before running any command."""
    console.print("\n[bold cyan]===== ROVA VEHICLE RENTAL MANAGEMENT =====[/bold cyan]")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user, message = login(username, password)
    if not user:
        console.print(f"[red]✗ {message}[/red]")
        sys.exit(1)
    console.print(f"[green]✓ {message}[/green]\n")
    set_current_user(user)
    return user


def build_parser():
    parser = argparse.ArgumentParser(
        prog="rova",
        description="Rova — Vehicle Rental Management System",
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # Auth
    sub.add_parser("register", help="Register a new user account")

    # Vehicles
    sub.add_parser("add-vehicle", help="Add a new vehicle to the fleet")
    p = sub.add_parser("list-vehicles", help="List all vehicles")
    p.add_argument("--type", dest="vehicle_type", default=None, help="Filter by type: car, motorbike, truck, bus")
    sub.add_parser("search-vehicle", help="Search for a vehicle by ID or plate")

    # Customers
    sub.add_parser("add-customer", help="Add a new customer")
    sub.add_parser("list-customers", help="List all customers")

    # Bookings
    sub.add_parser("create-booking", help="Book a vehicle for a customer")
    sub.add_parser("list-bookings", help="View all bookings")
    sub.add_parser("cancel-booking", help="Cancel an active booking")

    return parser


if __name__ == "__main__":
    seed_admin()
    parser = build_parser()
    args = parser.parse_args()

    # Register doesn't need login
    if args.command == "register":
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        success, message = register(username, password, role="user")
        if success:
            console.print(f"[green]✓ {message}[/green]")
        else:
            console.print(f"[red]✗ {message}[/red]")
        sys.exit(0)

    # All other commands require login first
    authenticate()

    if args.command == "add-vehicle":
        add_vehicle()
    elif args.command == "list-vehicles":
        list_vehicles()
    elif args.command == "search-vehicle":
        search_vehicle()
    elif args.command == "add-customer":
        add_customer()
    elif args.command == "list-customers":
        list_customers()
    elif args.command == "create-booking":
        create_booking()
    elif args.command == "list-bookings":
        list_bookings()
    elif args.command == "cancel-booking":
        cancel_booking()
