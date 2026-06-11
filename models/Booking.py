import uuid
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

class Booking:
    count = 0

    def __init__(self, id, customer_id, vehicle_id, start_date, end_date, total_cost, status="active"):
        self.id = id
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = float(total_cost)
        self._status = status
        Booking.count += 1

    # @property ensures status can only be 'active' or 'cancelled'
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in ["active", "cancelled"]:
            raise ValueError("Booking status must be 'active' or 'cancelled'.")
        self._status = value

    @staticmethod
    def calculate_cost(start_date, end_date, rate_per_day):
        """Calculate total rental cost from date range and daily rate."""
        start = datetime.strptime(start_date, DATE_FORMAT)
        end = datetime.strptime(end_date, DATE_FORMAT)
        days = (end - start).days
        if days <= 0:
            raise ValueError("End date must be after start date.")
        return days * rate_per_day

    def cancel(self):
        self._status = "cancelled"

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "vehicle_id": self.vehicle_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_cost": self.total_cost,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            customer_id=data["customer_id"],
            vehicle_id=data["vehicle_id"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            total_cost=data["total_cost"],
            status=data.get("status", "active"),
        )

    @classmethod
    def find_by_id(cls, booking_id, bookings):
        for b in bookings:
            if b.id == booking_id:
                return b
        return None

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    def __repr__(self):
        return (
            f"Booking(id={self.id!r}, customer={self.customer_id!r}, "
            f"vehicle={self.vehicle_id!r}, {self.start_date} → {self.end_date}, "
            f"KES {self.total_cost}, {self._status})"
        )

    def __str__(self):
        return self.__repr__()

