import json
import os

from models.Vehicle import Vehicle

DATA_FOLDER = "data"
VEHICLE_FILE = os.path.join(DATA_FOLDER, "vehicle.json")


def create_sample_vehicles():
    """
    Creates sample vehicle data if vehicle.json
    does not already exist.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    if os.path.exists(VEHICLE_FILE):
        print("Sample vehicles already exist.")
        return

    vehicles = [
        Vehicle(
            owner="brian",
            category="Car",
            brand="Toyota",
            model="Corolla",
            year=2022,
            price_per_day=3500,
        ),
        Vehicle(
            owner="mary",
            category="Motorbike",
            brand="Honda",
            model="CBR 250R",
            year=2021,
            price_per_day=1500,
        ),
        Vehicle(
            owner="john",
            category="Bus",
            brand="Isuzu",
            model="NQR",
            year=2020,
            price_per_day=12000,
        ),
        Vehicle(
            owner="alice",
            category="Truck",
            brand="Mercedes-Benz",
            model="Actros",
            year=2023,
            price_per_day=18000,
        ),
        Vehicle(
            owner="kevin",
            category="Car",
            brand="Mazda",
            model="Demio",
            year=2019,
            price_per_day=2800,
        ),
    ]

    with open(VEHICLE_FILE, "w") as file:
        json.dump(
            [vehicle.to_dict() for vehicle in vehicles],
            file,
            indent=4,
        )

    print("Sample vehicle data created successfully.")


if __name__ == "__main__":
    create_sample_vehicles()