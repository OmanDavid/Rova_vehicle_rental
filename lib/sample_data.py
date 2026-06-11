"""
sample_data.py — Seeds the database with vehicles, customers, and a default admin.
Run once before using the app: python lib/sample_data.py
"""

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.Vehicle import Vehicle
from models.Customer import Customer
from utils.auth import seed_admin, register

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

vehicles = [
    Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000),
    Vehicle(id="v002", make="Kawasaki", model="Ninja", year="2023", plate="KBD 202B", vehicle_type="motorbike", rate_per_day=2500),
    Vehicle(id="v003", make="Honda", model="Civic", year="2021", plate="KAA 555C", vehicle_type="car", rate_per_day=5000),
    Vehicle(id="v004", make="Toyota", model="Coaster", year="2020", plate="KCA 100D", vehicle_type="bus", rate_per_day=15000),
    Vehicle(id="v005", make="Subaru", model="Outback", year="2022", plate="KDB 303E", vehicle_type="car", rate_per_day=6500),
]

customers = [
    Customer(id="c001", name="Alex Mwangi", email="alex@rova.co.ke", phone="0712345678"),
    Customer(id="c002", name="Aisha Kamau", email="aisha@rova.co.ke", phone="0798765432"),
    Customer(id="c003", name="Brian Otieno", email="brian@rova.co.ke", phone="0756789012"),
]

with open(os.path.join(DATA_DIR, "vehicle.json"), "w") as f:
    json.dump([v.to_dict() for v in vehicles], f, indent=4)

with open(os.path.join(DATA_DIR, "customers.json"), "w") as f:
    json.dump([c.to_dict() for c in customers], f, indent=4)

with open(os.path.join(DATA_DIR, "bookings.json"), "w") as f:
    json.dump([], f, indent=4)

# Seed default admin + a regular user
with open(os.path.join(DATA_DIR, "users.json"), "w") as f:
    json.dump([], f, indent=4)

seed_admin()
register("john", "john123", role="user")

print("✓ Sample data loaded.")
print("  Admin login  → username: admin   password: admin123")
print("  User login   → username: john    password: john123")