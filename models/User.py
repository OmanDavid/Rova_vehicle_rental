import uuid


VALID_ROLES = ["admin", "user"]


class User:
    """
    Represents an authenticated system user.
    Roles: 'admin' (full access) or 'user' (view + book only).
    """

    count = 0

    def __init__(self, id, username, password_hash, role="user"):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self._role = role
        User.count += 1

    # @property ensures role can only be 'admin' or 'user'
    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in VALID_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(VALID_ROLES)}")
        self._role = value

    def is_admin(self):
        """Return True if this user has admin privileges."""
        return self._role == "admin"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self._role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            username=data["username"],
            password_hash=data["password_hash"],
            role=data.get("role", "user"),
        )

    @classmethod
    def find_by_username(cls, username, users):
        """Find a user by username (case-insensitive)."""
        for u in users:
            if u.username.lower() == username.lower():
                return u
        return None

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, role={self._role!r})"

    def __str__(self):
        return f"{self.username} [{self._role}]"