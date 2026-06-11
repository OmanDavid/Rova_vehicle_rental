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