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
