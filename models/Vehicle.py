import uuid

VALID_TYPES = ["car", "motorbike", "truck", "bus"]

class Vehicle:
    """
    Represents a vehicle that can be listed for booking.
    """

    def __init__(
        self,
        id,
        make,
        model,
        year,
        plate,
        vehicle_type,
        rate_per_day,
        available=True,
    ):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.plate = plate
        self.vehicle_type = vehicle_type
        self.rate_per_day = rate_per_day
        self.available = available

    @property
    def rate_per_day(self):
        return self._rate_per_day
    
    @rate_per_day.setter
    def rate_per_day(self, value):
        value = float(value)

        if value < 0:
            raise ValueError("Rate per day cannot be negative.")

        self._rate_per_day = value

    @property
    def vehicle_type(self):
        return self._vehicle_type
    
    @vehicle_type.setter
    def vehicle_type(self, value):
        value = value.lower()

        if value not in VALID_TYPES:
            raise ValueError(
                f"Vehicle type must be one of: {', '.join(VALID_TYPES)}"
            )

        self._vehicle_type = value

    def book(self):
        """Mark vehicle as booked."""
        self.available = False

    def release(self):
        """Mark vehicle as available."""
        self.available = True

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "plate": self.plate,
            "vehicle_type": self.vehicle_type,
            "rate_per_day": self.rate_per_day,
            "available": self.available,
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
        """
        Find a vehicle by its ID.
        """
        for vehicle in vehicles:
            if vehicle.id == vehicle_id:
                return vehicle
        return None
    
    @classmethod
    def find_by_plate(cls, plate, vehicles):
        """
        Find a vehicle by its number plate.
        """
        for vehicle in vehicles:
            if vehicle.plate.lower() == plate.lower():
                return vehicle
        return None
    
    @staticmethod
    def generate_id():
        """
        Generate a short unique vehicle ID.
        """
        return str(uuid.uuid4())[:8]

    

