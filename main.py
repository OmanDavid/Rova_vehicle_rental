"""
main.py — Rova CLI entry point.
Runs an interactive menu loop with role-based access.
"""

from rich.console import Console
from utils.auth import register, login, seed_admin
from utils.decorators import set_current_user, get_current_user, logout
from lib.functions import (
    add_vehicle, list_vehicles, search_vehicle,
    add_customer, list_customers,
    create_booking, list_bookings, cancel_booking,
)

console = Console()


def print_header():
    console.print("\n[bold cyan]===== ROVA VEHICLE RENTAL MANAGEMENT =====[/bold cyan]")


def auth_menu():
    """Login / Register screen shown before the main menu."""
    while True:
        print_header()
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user, message = login(username, password)
            if user:
                console.print(f"[green]✓ {message}[/green]")
                set_current_user(user)
                return user
            else:
                console.print(f"[red]✗ {message}[/red]")

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, message = register(username, password, role="user")
            if success:
                console.print(f"[green]✓ {message} Please log in.[/green]")
            else:
                console.print(f"[red]✗ {message}[/red]")

        elif choice == "3":
            console.print("[cyan]Goodbye![/cyan]")
            exit()

        else:
            console.print("[yellow]Invalid choice. Enter 1, 2, or 3.[/yellow]")


def admin_menu():
    """Full menu for admin users."""
    while True:
        user = get_current_user()
        print_header()
        console.print(f"[dim]Logged in as: {user.username} [admin][/dim]")
        print("\n--- Vehicles ---")
        print("1. Add Vehicle")
        print("2. View Vehicles")
        print("3. Search Vehicle")
        print("\n--- Customers ---")
        print("4. Add Customer")
        print("5. View Customers")
        print("\n--- Bookings ---")
        print("6. Create Booking")
        print("7. View Bookings")
        print("8. Cancel Booking")
        print("\n9. Logout")
        print("0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            add_vehicle()
        elif choice == "2":
            list_vehicles()
        elif choice == "3":
            search_vehicle()
        elif choice == "4":
            add_customer()
        elif choice == "5":
            list_customers()
        elif choice == "6":
            create_booking()
        elif choice == "7":
            list_bookings()
        elif choice == "8":
            cancel_booking()
        elif choice == "9":
            logout()
            console.print("[cyan]Logged out.[/cyan]")
            return
        elif choice == "0":
            console.print("[cyan]Goodbye![/cyan]")
            exit()
        else:
            console.print("[yellow]Invalid choice.[/yellow]")


def user_menu():
    """Limited menu for regular users."""
    while True:
        user = get_current_user()
        print_header()
        console.print(f"[dim]Logged in as: {user.username} [user][/dim]")
        print("\n1. View Vehicles")
        print("2. Search Vehicle")
        print("3. Create Booking")
        print("4. View Bookings")
        print("\n5. Logout")
        print("0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            list_vehicles()
        elif choice == "2":
            search_vehicle()
        elif choice == "3":
            create_booking()
        elif choice == "4":
            list_bookings()
        elif choice == "5":
            logout()
            console.print("[cyan]Logged out.[/cyan]")
            return
        elif choice == "0":
            console.print("[cyan]Goodbye![/cyan]")
            exit()
        else:
            console.print("[yellow]Invalid choice.[/yellow]")


if __name__ == "__main__":
    # Create default admin account on first run
    seed_admin()

    while True:
        user = auth_menu()
        if user.is_admin():
            admin_menu()
        else:
            user_menu()