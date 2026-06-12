# Rova — Vehicle Rental Management System

A command-line vehicle rental management tool built with Python. Manage vehicles, customers, and bookings from the terminal with role-based authentication.

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/OmanDavid/Rova_vehicle_rental.git
cd Rova_vehicle_rental
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed sample data (first time only)
```bash
python lib/sample_data.py
```

### 5. Run the app
```bash
python main.py <command>
```

---

## Default Credentials

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |
| User  | john     | john123   |

---

## Commands

Every command asks for your username and password first, then runs the action.

```bash
# See all available commands
python main.py --help

# Register a new user account
python main.py register

# Vehicles
python main.py add-vehicle
python main.py list-vehicles
python main.py list-vehicles --type car
python main.py search-vehicle

# Customers
python main.py add-customer
python main.py list-customers

# Bookings
python main.py create-booking
python main.py list-bookings
python main.py cancel-booking
```

---

## Access Control

| Command | Who can use it |
|---|---|
| `add-vehicle` | Admin only |
| `list-vehicles` | Everyone |
| `search-vehicle` | Everyone |
| `add-customer` | Admin only |
| `list-customers` | Everyone |
| `create-booking` | Must be logged in |
| `list-bookings` | Must be logged in |
| `cancel-booking` | Admin only |

---

## Project Structure

```
Rova_vehicle_rental/
├── main.py                  # CLI entry point (argparse)
├── models/
│   ├── Vehicle.py           # Vehicle class (@property on available)
│   ├── Customer.py          # Customer class
│   ├── Booking.py           # Booking class (@property on status)
│   └── User.py              # Auth user class (@property on role)
├── lib/
│   ├── functions.py         # All CLI action functions
│   └── sample_data.py       # Seeds database with test data
├── utils/
│   ├── auth.py              # Registration, login, bcrypt password hashing
│   ├── decorators.py        # @require_login, @admin_only, @log_action
│   └── helpers.py           # Input validation helpers
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
- argparse subcommands for all actions
- Login required before every command
- Role-based access — Admin vs User
- Add and list vehicles filtered by type (car, motorbike, truck, bus)
- Register customers with duplicate email detection
- Create bookings with automatic cost calculation
- Availability guard — can't double-book a vehicle
- Cancel bookings — vehicle automatically freed up
- All data persisted in JSON files
- Rich color-coded tables in the terminal
- 30 unit tests

---

## External Packages

| Package | Purpose |
|---------|---------|
| `rich`  | Colored tables and styled terminal output |
| `bcrypt`| Secure password hashing |
| `pytest`| Unit testing |

---

## Known Issues
- No booking overlap detection yet
- No password change feature
- Sessions don't persist — login required for every command

---

## Authors
Built as a Moringa School Python group summative lab.