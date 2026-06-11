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
