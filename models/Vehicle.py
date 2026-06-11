import uuid

VALID_TYPES = ["car", "motorbike", "truck", "bus"]


class Vehicle:
    # Tracks how many vehicles have been created this session
    count = 0

    def __init__(self, id, make, model, year, plate, vehicle_type, rate_per_day, available=True):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.plate = plate
        self.vehicle_type = vehicle_type
        self.rate_per_day = float(rate_per_day)
        self._available = available
        Vehicle.count += 1

    # @property controls access to available — can only be set to True/False
    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        if not isinstance(value, bool):
            raise ValueError("Available must be True or False.")
        self._available = value

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "plate": self.plate,
            "vehicle_type": self.vehicle_type,
            "rate_per_day": self.rate_per_day,
            "available": self._available,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            make=data["make"],
            model=data["model"],
            year=data["year"],
            plate=data["plate"],
            vehicle_type=data["vehicle_type"],
            rate_per_day=data["rate_per_day"],
            available=data.get("available", True),
        )

    @classmethod
    def find_by_id(cls, vehicle_id, vehicles):
        for v in vehicles:
            if v.id == vehicle_id:
                return v
        return None

    @classmethod
    def find_by_plate(cls, plate, vehicles):
        for v in vehicles:
            if v.plate.lower() == plate.lower():
                return v
        return None

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    def __repr__(self):
        status = "Available" if self._available else "Booked"
        return f"[{self.vehicle_type.upper()}] {self.year} {self.make} {self.model} | {self.plate} | KES {self.rate_per_day}/day | {status}"

    def __str__(self):
        return self.__repr__()