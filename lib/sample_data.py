import json
import os

from models.User import User
from models.Vehicle import Vehicle
from models.Customer import Customer
from models.Booking import Booking
from utils.auth import hash_password

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
VEHICLES_FILE = os.path.join(DATA_DIR, "vehicle.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")

os.makedirs(DATA_DIR, exist_ok=True)

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ------------------------------------------------------------------
# Sample Users
# ------------------------------------------------------------------

users = [
    User(
        id=User.generate_id(),
        username="admin",
        password_hash=hash_password("admin123"),
        role="admin",
    ),
    User(
        id=User.generate_id(),
        username="john",
        password_hash=hash_password("password123"),
        role="user",
    ),
]

write_json(
    USERS_FILE,
    [user.to_dict() for user in users],
)

# ------------------------------------------------------------------
# Sample Vehicles
# ------------------------------------------------------------------

vehicles = [
    Vehicle(
        id=Vehicle.generate_id(),
        make="Toyota",
        model="Corolla",
        year=2022,
        plate="KDA123A",
        vehicle_type="car",
        rate_per_day=3500,
        available=True,
    ),
    Vehicle(
        id=Vehicle.generate_id(),
        make="Isuzu",
        model="FRR",
        year=2021,
        plate="KDB456B",
        vehicle_type="truck",
        rate_per_day=9000,
        available=True,
    ),
    Vehicle(
        id=Vehicle.generate_id(),
        make="Yamaha",
        model="FZ",
        year=2023,
        plate="KMC789C",
        vehicle_type="motorbike",
        rate_per_day=1500,
        available=True,
    ),
    Vehicle(
        id=Vehicle.generate_id(),
        make="Scania",
        model="K360",
        year=2020,
        plate="KBT321D",
        vehicle_type="bus",
        rate_per_day=12000,
        available=True,
    ),
]

write_json(
    VEHICLES_FILE,
    [vehicle.to_dict() for vehicle in vehicles],
)

# ------------------------------------------------------------------
# Sample Customers
# ------------------------------------------------------------------

customers = [
    Customer(
        id=Customer.generate_id(),
        name="Alice Wanjiku",
        email="alice@example.com",
        phone="0712345678",
    ),
    Customer(
        id=Customer.generate_id(),
        name="Brian Otieno",
        email="brian@example.com",
        phone="0723456789",
    ),
]

write_json(
    CUSTOMERS_FILE,
    [customer.to_dict() for customer in customers],
)