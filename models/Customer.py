import uuid


class Customer:
    count = 0

    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        Customer.count += 1

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )

    @classmethod
    def find_by_id(cls, customer_id, customers):
        for c in customers:
            if c.id == customer_id:
                return c
        return None

    @classmethod
    def find_by_name(cls, name, customers):
        for c in customers:
            if c.name.lower() == name.lower():
                return c
        return None

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    def __repr__(self):
        return f"Customer(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r})"

    def __str__(self):
        return f"{self.name} | {self.email} | {self.phone}"