import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.Vehicle import Vehicle
from models.Customer import Customer
from models.Booking import Booking
from models.User import User


# ── Vehicle tests ─────────────────────────────────────────────────────────────

def test_vehicle_creation():
    v = Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000)
    assert v.make == "Toyota"
    assert v.available == True

def test_vehicle_available_setter():
    v = Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000)
    v.available = False
    assert v.available == False

def test_vehicle_available_setter_invalid():
    v = Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000)
    with pytest.raises(ValueError):
        v.available = "yes"

def test_vehicle_to_dict():
    v = Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000)
    assert v.to_dict()["make"] == "Toyota"

def test_vehicle_from_dict():
    data = {"id": "v001", "make": "Toyota", "model": "Hilux", "year": "2022", "plate": "KBC 001A", "vehicle_type": "truck", "rate_per_day": 8000, "available": True}
    v = Vehicle.from_dict(data)
    assert v.rate_per_day == 8000.0

def test_vehicle_find_by_id():
    vehicles = [Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000)]
    assert Vehicle.find_by_id("v001", vehicles).make == "Toyota"

def test_vehicle_find_by_plate():
    vehicles = [Vehicle(id="v001", make="Toyota", model="Hilux", year="2022", plate="KBC 001A", vehicle_type="truck", rate_per_day=8000)]
    assert Vehicle.find_by_plate("kbc 001a", vehicles).id == "v001"

def test_vehicle_not_found():
    assert Vehicle.find_by_id("v999", []) is None


# ── Customer tests ────────────────────────────────────────────────────────────

def test_customer_creation():
    c = Customer(id="c001", name="Alex", email="alex@dev.com", phone="0712345678")
    assert c.name == "Alex"

def test_customer_to_dict():
    c = Customer(id="c001", name="Alex", email="alex@dev.com", phone="0712345678")
    assert c.to_dict()["email"] == "alex@dev.com"

def test_customer_from_dict():
    c = Customer.from_dict({"id": "c001", "name": "Alex", "email": "alex@dev.com", "phone": "0712345678"})
    assert c.id == "c001"

def test_customer_find_by_id():
    customers = [Customer(id="c001", name="Alex", email="alex@dev.com", phone="0712345678")]
    assert Customer.find_by_id("c001", customers).name == "Alex"

def test_customer_find_by_name():
    customers = [Customer(id="c001", name="Alex", email="alex@dev.com", phone="0712345678")]
    assert Customer.find_by_name("alex", customers).id == "c001"

def test_customer_not_found():
    assert Customer.find_by_id("c999", []) is None


# ── Booking tests ─────────────────────────────────────────────────────────────

def test_booking_creation():
    b = Booking(id="b001", customer_id="c001", vehicle_id="v001", start_date="2025-07-01", end_date="2025-07-05", total_cost=20000)
    assert b.status == "active"

def test_booking_cancel():
    b = Booking(id="b001", customer_id="c001", vehicle_id="v001", start_date="2025-07-01", end_date="2025-07-05", total_cost=20000)
    b.cancel()
    assert b.status == "cancelled"

def test_booking_status_invalid():
    b = Booking(id="b001", customer_id="c001", vehicle_id="v001", start_date="2025-07-01", end_date="2025-07-05", total_cost=20000)
    with pytest.raises(ValueError):
        b.status = "pending"

def test_booking_calculate_cost():
    assert Booking.calculate_cost("2025-07-01", "2025-07-05", 5000) == 20000

def test_booking_invalid_dates():
    with pytest.raises(ValueError):
        Booking.calculate_cost("2025-07-05", "2025-07-01", 5000)

def test_booking_to_dict():
    b = Booking(id="b001", customer_id="c001", vehicle_id="v001", start_date="2025-07-01", end_date="2025-07-05", total_cost=20000)
    assert b.to_dict()["status"] == "active"

def test_booking_find_by_id():
    bookings = [Booking(id="b001", customer_id="c001", vehicle_id="v001", start_date="2025-07-01", end_date="2025-07-05", total_cost=20000)]
    assert Booking.find_by_id("b001", bookings).customer_id == "c001"


# ── User tests ────────────────────────────────────────────────────────────────

def test_user_creation():
    u = User(id="u001", username="admin", password_hash="hashed", role="admin")
    assert u.username == "admin"
    assert u.is_admin() == True

def test_user_role_setter_valid():
    u = User(id="u001", username="john", password_hash="hashed", role="user")
    u.role = "admin"
    assert u.role == "admin"

def test_user_role_setter_invalid():
    u = User(id="u001", username="john", password_hash="hashed", role="user")
    with pytest.raises(ValueError):
        u.role = "superuser"

def test_user_is_admin_false():
    u = User(id="u001", username="john", password_hash="hashed", role="user")
    assert u.is_admin() == False

def test_user_to_dict():
    u = User(id="u001", username="john", password_hash="hashed", role="user")
    assert u.to_dict()["username"] == "john"

def test_user_from_dict():
    u = User.from_dict({"id": "u001", "username": "john", "password_hash": "hashed", "role": "user"})
    assert u.role == "user"

def test_user_find_by_username():
    users = [User(id="u001", username="admin", password_hash="hashed", role="admin")]
    assert User.find_by_username("ADMIN", users).id == "u001"

def test_user_not_found():
    assert User.find_by_username("ghost", []) is None


# ── Auth tests ────────────────────────────────────────────────────────────────

def test_password_hashing():
    from utils.auth import hash_password, check_password
    hashed = hash_password("secret123")
    assert check_password("secret123", hashed) == True
    assert check_password("wrongpass", hashed) == False