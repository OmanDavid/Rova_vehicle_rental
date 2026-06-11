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
        self._vehicle_id = vehicle_id or str(uuid.uuid4())[:8]
        self.owner = owner
        self.category = category
        self.brand = brand
        self.model = model
        self.year = year
        self.price_per_day = price_per_day
        self.available = available

    @property
    def vehicle_id(self):
        return self._vehicle_id
    
    @property
    def price_per_day(self):
        return self._price_per_day
    
    @price_per_day.setter
    def price_per_day(self, value):
        if value < 0:
            raise ValueError("Price per day cannot be negative.")
        self._price_per_day = value
