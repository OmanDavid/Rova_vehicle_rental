import json

class Booking:
    FILE_PATH = "data/bookings.json"
    all_bookings = []
    booking_counter = 1

    def __init__(self, customer_name, vehicle, days, status= "active", booking_id = None):
        self.customer_name = customer_name
        self.vehicle = vehicle
        self.days = int(days)

        if self.days <= 0:
            raise ValueError("Days must be greater than 0.")

        self.first_pay = 200
        self.extra_pay = self.days * 200
        self.total_cost = self.first_pay + self.extra_pay

        self.status = status


        self.booking_id = (
            booking_id
            if booking_id is not None
            else Booking.booking_counter
       
        )

        if self.booking_id is None:
           Booking.booking_counter += 1

        Booking.all_bookings.append(self)

# Status validation
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in ["active", "cancelled"]:
            raise ValueError(
                "Booking status must be 'active' or 'cancelled'."
            )
        self._status = value

    def cancel(self):
        self.status = "cancelled"

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "vehicle": self.vehicle,
            "days" : self.days,
            "first_pay": self.first_pay,
            "extra_pay": self.extra_pay,
            "total_cost": self.total_cost,
            "status": self.status,
        }


    def save_to_json(self):
        try:
            try:
                with open(self.FILE_PATH, "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            data.append(self.to_dict())

            with open(self.FILE_PATH, "w") as f:
                json.dump(data, f, indent=4)

            print(f"{self.booking_id} saved successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")


