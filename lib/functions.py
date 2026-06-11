"""
functions.py — All CLI action functions for Rova.
Each function maps to a menu option in main.py.
Admin-only actions are protected with @admin_only.
All booking actions require @require_login.
"""

import json
import os
from rich.console import Console
from rich.table import Table
from rich import box

from models.Vehicle import Vehicle, VALID_TYPES
from models.Customer import Customer
from models.Booking import Booking, DATE_FORMAT
from utils.decorators import require_login, admin_only, log_action
from utils.helpers import prompt, prompt_float, prompt_int, prompt_date, prompt_choice

console = Console()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
VEHICLES_FILE = os.path.join(DATA_DIR, "vehicle.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")


# ── File I/O ──────────────────────────────────────────────────────────────────

def load(filepath):
    """Load a JSON file and return its contents as a list."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        console.print(f"[yellow]Warning: could not parse {filepath} — starting fresh.[/yellow]")
        return []


def save(filepath, data):
    """Save a list of dicts to a JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# ── Vehicle functions (Admin only) ────────────────────────────────────────────

@admin_only
@log_action
def add_vehicle(current_user):
    """Prompt admin to add a new vehicle to the fleet."""
    print("\n--- Add Vehicle ---")
    make = prompt("Make (e.g. Toyota)")
    model = prompt("Model (e.g. Hilux)")
    year = prompt("Year")
    plate = prompt("Number Plate (e.g. KBC 001A)")
    vehicle_type = prompt_choice("Type", VALID_TYPES)
    rate_per_day = prompt_float("Rate Per Day (KES)")

    vehicles = [Vehicle.from_dict(v) for v in load(VEHICLES_FILE)]

    if Vehicle.find_by_plate(plate, vehicles):
        console.print(f"[red]✗ A vehicle with plate '{plate}' already exists.[/red]")
        return

    vehicle = Vehicle(
        id=Vehicle.generate_id(),
        make=make, model=model, year=year, plate=plate,
        vehicle_type=vehicle_type, rate_per_day=rate_per_day,
    )
    vehicles.append(vehicle)
    save(VEHICLES_FILE, [v.to_dict() for v in vehicles])
    console.print(f"[green]✓ Vehicle '{make} {model}' added successfully. ID: {vehicle.id}[/green]")


@log_action
def list_vehicles(current_user=None):
    """Display all vehicles in a rich table."""
    vehicles = [Vehicle.from_dict(v) for v in load(VEHICLES_FILE)]

    vehicle_type = input("Filter by type (leave blank for all): ").strip().lower()
    if vehicle_type:
        vehicles = [v for v in vehicles if v.vehicle_type == vehicle_type]

    if not vehicles:
        console.print("[yellow]No vehicles found.[/yellow]")
        return

    table = Table(title="===== ROVA FLEET =====", box=box.ROUNDED)
    table.add_column("ID", style="dim")
    table.add_column("Type", style="cyan")
    table.add_column("Make & Model", style="bold")
    table.add_column("Year")
    table.add_column("Plate")
    table.add_column("KES/Day", style="yellow")
    table.add_column("Status")

    for v in vehicles:
        status = "[green]Available[/green]" if v.available else "[red]Booked[/red]"
        table.add_row(v.id, v.vehicle_type, f"{v.make} {v.model}", str(v.year), v.plate, str(v.rate_per_day), status)

    console.print(table)


@log_action
def search_vehicle(current_user=None):
    """Search for a vehicle by ID or plate."""
    print("\n--- Search Vehicle ---")
    query = prompt("Enter Vehicle ID or Plate")
    vehicles = [Vehicle.from_dict(v) for v in load(VEHICLES_FILE)]

    result = Vehicle.find_by_id(query, vehicles) or Vehicle.find_by_plate(query, vehicles)

    if not result:
        console.print(f"[red]✗ No vehicle found for '{query}'.[/red]")
        return

    console.print(f"\n[bold]Vehicle Found:[/bold]")
    console.print(f"  ID       : {result.id}")
    console.print(f"  Type     : {result.vehicle_type}")
    console.print(f"  Vehicle  : {result.make} {result.model} ({result.year})")
    console.print(f"  Plate    : {result.plate}")
    console.print(f"  Rate     : KES {result.rate_per_day}/day")
    status = "[green]Available[/green]" if result.available else "[red]Currently Booked[/red]"
    console.print(f"  Status   : {status}")


# ── Customer functions (Admin only) ──────────────────────────────────────────

@admin_only
@log_action
def add_customer(current_user):
    """Prompt admin to register a new customer."""
    print("\n--- Add Customer ---")
    name = prompt("Full Name")
    email = prompt("Email")
    phone = prompt("Phone")

    customers = [Customer.from_dict(c) for c in load(CUSTOMERS_FILE)]

    if any(c.email.lower() == email.lower() for c in customers):
        console.print(f"[red]✗ A customer with email '{email}' already exists.[/red]")
        return

    customer = Customer(id=Customer.generate_id(), name=name, email=email, phone=phone)
    customers.append(customer)
    save(CUSTOMERS_FILE, [c.to_dict() for c in customers])
    console.print(f"[green]✓ Customer '{name}' added. ID: {customer.id}[/green]")


@log_action
def list_customers(current_user=None):
    """Display all registered customers."""
    customers = [Customer.from_dict(c) for c in load(CUSTOMERS_FILE)]

    if not customers:
        console.print("[yellow]No customers found.[/yellow]")
        return

    table = Table(title="===== CUSTOMERS =====", box=box.ROUNDED)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Email", style="cyan")
    table.add_column("Phone")

    for c in customers:
        table.add_row(c.id, c.name, c.email, c.phone)

    console.print(table)


# ── Booking functions ─────────────────────────────────────────────────────────

@require_login
@log_action
def create_booking(current_user):
    """Book a vehicle for a customer."""
    print("\n--- Book Vehicle ---")

    # Show available vehicles first
    vehicles = [Vehicle.from_dict(v) for v in load(VEHICLES_FILE)]
    available = [v for v in vehicles if v.available]

    if not available:
        console.print("[red]✗ No vehicles are currently available.[/red]")
        return

    console.print("[cyan]Available Vehicles:[/cyan]")
    for v in available:
        console.print(f"  {v.id} — {v.make} {v.model} ({v.vehicle_type}) — KES {v.rate_per_day}/day")

    vehicle_id = prompt("\nVehicle ID")
    vehicle = Vehicle.find_by_id(vehicle_id, vehicles)

    if not vehicle:
        console.print(f"[red]✗ Vehicle ID '{vehicle_id}' not found.[/red]")
        return

    if not vehicle.available:
        console.print(f"[red]✗ '{vehicle.make} {vehicle.model}' is currently booked.[/red]")
        return

    # Show customers
    customers = [Customer.from_dict(c) for c in load(CUSTOMERS_FILE)]
    if not customers:
        console.print("[red]✗ No customers registered. Add a customer first.[/red]")
        return

    console.print("\n[cyan]Registered Customers:[/cyan]")
    for c in customers:
        console.print(f"  {c.id} — {c.name}")

    customer_id = prompt("\nCustomer ID")
    customer = Customer.find_by_id(customer_id, customers)

    if not customer:
        console.print(f"[red]✗ Customer ID '{customer_id}' not found.[/red]")
        return

    start_date = prompt_date("Start Date")
    end_date = prompt_date("End Date")

    try:
        total_cost = Booking.calculate_cost(start_date, end_date, vehicle.rate_per_day)
    except ValueError as e:
        console.print(f"[red]✗ {e}[/red]")
        return

    days = int(total_cost / vehicle.rate_per_day)

    booking = Booking(
        id=Booking.generate_id(),
        customer_id=customer_id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date,
        total_cost=total_cost,
    )

    bookings = [Booking.from_dict(b) for b in load(BOOKINGS_FILE)]
    bookings.append(booking)
    save(BOOKINGS_FILE, [b.to_dict() for b in bookings])

    vehicle.available = False
    save(VEHICLES_FILE, [v.to_dict() for v in vehicles])

    print()
    console.print(f"[green]✓ Booking successful![/green]")
    console.print(f"  Booking ID  : {booking.id}")
    console.print(f"  Customer    : {customer.name}")
    console.print(f"  Vehicle     : {vehicle.make} {vehicle.model}")
    console.print(f"  Days        : {days}")
    console.print(f"  Total Cost  : KES {total_cost}")


@require_login
@log_action
def list_bookings(current_user):
    """Display all bookings."""
    bookings = [Booking.from_dict(b) for b in load(BOOKINGS_FILE)]
    customers = {c["id"]: c["name"] for c in load(CUSTOMERS_FILE)}
    vehicles = {v["id"]: f"{v['make']} {v['model']}" for v in load(VEHICLES_FILE)}

    if not bookings:
        console.print("[yellow]No bookings found.[/yellow]")
        return

    table = Table(title="===== BOOKINGS =====", box=box.ROUNDED)
    table.add_column("Booking ID", style="dim")
    table.add_column("Customer", style="bold")
    table.add_column("Vehicle", style="cyan")
    table.add_column("Start")
    table.add_column("End")
    table.add_column("Total (KES)", style="yellow")
    table.add_column("Status")

    for b in bookings:
        color = "green" if b.status == "active" else "red"
        table.add_row(
            b.id,
            customers.get(b.customer_id, b.customer_id),
            vehicles.get(b.vehicle_id, b.vehicle_id),
            b.start_date, b.end_date,
            str(b.total_cost),
            f"[{color}]{b.status}[/{color}]",
        )

    console.print(table)


@admin_only
@log_action
def cancel_booking(current_user):
    """Cancel an active booking and free the vehicle."""
    print("\n--- Cancel Booking ---")
    booking_id = prompt("Booking ID")

    bookings = [Booking.from_dict(b) for b in load(BOOKINGS_FILE)]
    booking = Booking.find_by_id(booking_id, bookings)

    if not booking:
        console.print(f"[red]✗ Booking ID '{booking_id}' not found.[/red]")
        return

    if booking.status == "cancelled":
        console.print(f"[yellow]Booking '{booking_id}' is already cancelled.[/yellow]")
        return

    booking.cancel()
    save(BOOKINGS_FILE, [b.to_dict() for b in bookings])

    vehicles = [Vehicle.from_dict(v) for v in load(VEHICLES_FILE)]
    vehicle = Vehicle.find_by_id(booking.vehicle_id, vehicles)
    if vehicle:
        vehicle.available = True
        save(VEHICLES_FILE, [v.to_dict() for v in vehicles])

    console.print(f"[green]✓ Booking '{booking_id}' cancelled. Vehicle is now available.[/green]")