import uuid

class Vehicle:
    """
    Represents a vehicle that can be listed for booking.
    """

    def __init__(
        self,
        owner,
        category,
        brand,
        model,
        year,
        price_per_day,
        available=True,
        vehicle_id=None,
    ):