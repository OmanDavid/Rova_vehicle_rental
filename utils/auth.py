"""
auth.py — Handles user registration, login, and password hashing.
Uses bcrypt for secure password storage.
"""

import json
import os
import bcrypt
from models.User import User

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def load_users():
    """Load all users from users.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_users(users):
    """Save a list of User objects to users.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=4)


def hash_password(plain_password):
    """Hash a plain text password using bcrypt."""
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def check_password(plain_password, hashed):
    """Check a plain password against a bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())


def register(username, password, role="user"):
    """
    Register a new user.

    Args:
        username (str): Desired username.
        password (str): Plain text password (will be hashed).
        role (str): 'admin' or 'user'.

    Returns:
        (bool, str): Success status and message.
    """
    users = [User.from_dict(u) for u in load_users()]

    if User.find_by_username(username, users):
        return False, f"Username '{username}' is already taken."

    if len(password) < 4:
        return False, "Password must be at least 4 characters."

    hashed = hash_password(password)
    user = User(id=User.generate_id(), username=username, password_hash=hashed, role=role)
    users.append(user)
    save_users(users)
    return True, f"Account created for '{username}' as {role}."


def login(username, password):
    """
    Authenticate a user.

    Args:
        username (str): Username to look up.
        password (str): Plain text password to verify.

    Returns:
        (User or None, str): The logged-in User object or None, and a message.
    """
    users = [User.from_dict(u) for u in load_users()]
    user = User.find_by_username(username, users)

    if not user:
        return None, "Username not found."

    if not check_password(password, user.password_hash):
        return None, "Incorrect password."

    return user, f"Welcome back, {user.username}!"


def seed_admin():
    """
    Create a default admin account if no users exist.
    Called once on first run.
    """
    users = load_users()
    if not users:
        register(username="admin", password="admin123", role="admin")