import time
from random import randint
import random

from HelperLibrary.StorageFunctions import StorageFunctions
from BookingSystem.Book import BookStore

if __name__ == '__main__':
    booking_system = BookStore("drones")
    while True:
        lowest_jobs = StorageFunctions("world_data").retrieve(["items"], ["Drone jobs minimum"])
        lowest_jobs = (lowest_jobs[0])[1]
        highest_jobs = StorageFunctions("world_data").retrieve(["items"], ["Drone jobs maximum"])
        highest_jobs = (highest_jobs[0])[1]
        jobs = randint(lowest_jobs, highest_jobs)
        for _ in range(jobs):
            places_list = StorageFunctions("locations").list("name")
            origin = random.choice(places_list)
            places_list.remove(origin)
            destination = random.choice(places_list)
            result = booking_system.validate_cities(origin, destination)
            if result:
                drone = booking_system.find_available_drone(origin)
                if drone:
                    booking_system.assign_booking(drone, origin, destination, "emulator")
        time.sleep(360)
