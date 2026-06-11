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