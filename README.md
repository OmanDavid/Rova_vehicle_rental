# Rova — Vehicle Rental Management System

A command-line vehicle rental management tool built with Python OOP, interactive menus, and role-based authentication.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/OmanDavid/Rova_vehicle_rental.git
cd Rova_vehicle_rental
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed sample data

```bash
python lib/sample_data.py
```

### 4. Run the app

```bash
python main.py
```

---

## Default Credentials

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |
| User  | john     | john123   |

---

## CLI Flow

```
===== ROVA VEHICLE RENTAL MANAGEMENT =====

1. Login
2. Register
3. Exit

Choice: 1
Username: admin
Password: admin123
✓ Welcome back, admin!

--- Vehicles ---
1. Add Vehicle
2. View Vehicles
3. Search Vehicle

--- Customers ---
4. Add Customer
5. View Customers

--- Bookings ---
6. Create Booking
7. View Bookings
8. Cancel Booking

9. Logout
0. Exit
```

Regular users (role: user) only see: View Vehicles, Search Vehicle, Create Booking, View Bookings.

---

## Project Structure

```
Rova_vehicle_rental/
├── main.py                  # Interactive menu loop + auth flow
├── models/
│   ├── Vehicle.py           # Vehicle class (@property on available)
│   ├── Customer.py          # Customer class
│   ├── Booking.py           # Booking class (@property on status)
│   └── User.py              # Auth user class (@property on role)
├── lib/
│   ├── functions.py         # All CLI actions (decorated with @require_login / @admin_only)
│   └── sample_data.py       # Seeds database with test data
├── utils/
│   ├── auth.py              # Registration, login, bcrypt password hashing
│   ├── decorators.py        # @require_login, @admin_only, @log_action
│   └── helpers.py           # Input validation helpers (prompt, prompt_date, etc.)
├── data/
│   ├── vehicle.json
│   ├── customers.json
│   ├── bookings.json
│   └── users.json
├── tests/
│   └── test_models.py       # 30 pytest unit tests
├── requirements.txt
└── README.md
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## Features

- Interactive numbered menu (no commands to memorize)
- User registration and login with bcrypt password hashing
- Role-based access: Admin vs User
- Admins can add vehicles, manage customers, cancel bookings
- Users can view vehicles, search, and create bookings
- Availability guard — can't double-book a vehicle
- Auto cost calculation from date range × daily rate
- All data persisted in JSON files
- Rich color-coded tables
- 30 unit tests

## External Packages

| Package | Purpose |
|---------|---------|
| `rich`  | Colored tables and styled terminal output |
| `bcrypt`| Secure password hashing |
| `pytest`| Unit testing |

## Known Issues

- No password change feature yet
- Booking overlap detection not yet implemented (same vehicle, overlapping dates)