import re

def validate_username(username):
    if not username.strip():
        return False, "Incorrect username, try again!"
    return True, ""
    
def validate_password(password_hashed):
    if len(password_hashed) < 5:
        return False, "Password must be more than 5 characters long"
    return True, ""
    
