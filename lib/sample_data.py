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