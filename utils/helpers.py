import re

def validate_username(username):
    if not username.strip():
        return False, "Incorrect username, try again!"
    return True, ""



