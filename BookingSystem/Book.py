from datetime import datetime, timedelta
from random import randint

from HelperLibrary.StorageFunctions import StorageFunctions
from Drones.Drone import Drone


class BookStore:
    def __init__(self, table_name):
        self.table_name = table_name

    @staticmethod
    def get_list_of_locations():
        list_of_locations = StorageFunctions("locations").list("name")
        print("List of locations:")
        counter = 1
        for location_name in sorted(list_of_locations):
            print(counter, ":", location_name, end="\n")
            counter += 1

    @staticmethod
    def validate_cities(origin, destination):
        if origin != destination:
            list_of_locations = StorageFunctions("locations").list("name")
            if (origin in list_of_locations) and (destination in list_of_locations):
                return True, ""
            else:
                return False, "Invalid origin or destination"
        else:
            return False, "Origin cannot be same as destination"

    def find_available_drone(self, origin):
        location_data = StorageFunctions("locations").retrieve(["name"], [origin])
        origin_id = (location_data[0])[0]
        available_drones = StorageFunctions(self.table_name).retrieve(["location_id", "job"], [origin_id, False])
        if not available_drones:
            return None
        else:
            drone_data = available_drones[0]
            drone = Drone(drone_data[0], drone_data[1], drone_data[2], drone_data[3], drone_data[4], drone_data[5], drone_data[6], drone_data[7], drone_data[8], drone_data[9])
            return drone

    def assign_booking(self, drone, origin, destination, username):
        user_data = StorageFunctions("users").retrieve(["username"], [username])
        user_id = (user_data[0])[0]
        location_data = StorageFunctions("locations").retrieve(["name"], [origin])
        origin_id = (location_data[0])[0]
        location_data = StorageFunctions("locations").retrieve(["name"], [destination])
        destination_id = (location_data[0])[0]
        if origin_id < destination_id:
            route_data = StorageFunctions("routes").retrieve(["city_a", "city_b"], [origin_id, destination_id])
        else:
            route_data = StorageFunctions("routes").retrieve(["city_a", "city_b"], [destination_id, origin_id])
        route_id = (route_data[0])[0]
        job_start_time = datetime.now()
        job_duration = self._calculatejobduration((route_data[0])[1])
        job_finish_time = job_start_time + timedelta(minutes=job_duration)
        assert origin_id == drone.location_id
        StorageFunctions(self.table_name).update(["job", "user_id", "route_id", "job_start_time", "job_duration", "job_finish_time", "origin_id", "destination_id"], [True, user_id, route_id, job_start_time, job_duration, job_finish_time, origin_id, destination_id], drone.id)
        return "Booking successful!\nYour drone's number is: " + str(drone.id)

    @staticmethod
    def _calculatejobduration(distance):
        traffic_probability = StorageFunctions("world_data").retrieve(["items"], ["Traffic probability"])
        traffic_probability = (traffic_probability[0])[1]
        current_traffic = 100 - (randint(1, 100))
        if traffic_probability <= current_traffic:
            lowest_speed = StorageFunctions("world_data").retrieve(["items"], ["Drone lowest traffic speed"])
            lowest_speed = (lowest_speed[0])[1]
            highest_speed = StorageFunctions("world_data").retrieve(["items"], ["Drone highest traffic speed"])
            highest_speed = (highest_speed[0])[1]
            speed = randint(lowest_speed, highest_speed)
        else:
            lowest_speed = StorageFunctions("world_data").retrieve(["items"], ["Drone lowest speed"])
            lowest_speed = (lowest_speed[0])[1]
            highest_speed = StorageFunctions("world_data").retrieve(["items"], ["Drone highest speed"])
            highest_speed = (highest_speed[0])[1]
            speed = randint(lowest_speed, highest_speed)
        job_duration = distance/speed
        return int(job_duration*60)


class Book:
    def __init__(self, username, drones_table_name="drones"):
        self.username = username
        self.book_module = BookStore(drones_table_name)

    def initiate_booking(self):
        valid_input = False
        while not valid_input:
            try:
                list_choice = int(input("Enter 1 to get a list of places and 0 to continue without a list:"))
            except ValueError:
                print("Not a valid input")
            else:
                valid_input = True
        if list_choice:
            self.book_module.get_list_of_locations()
        origin = input("Enter origin name:")
        destination = input("Enter destination name:")
        origin = (origin.lower()).capitalize()
        destination = (destination.lower()).capitalize()
        result, message = self.book_module.validate_cities(origin, destination)
        if result:
            drone = self.book_module.find_available_drone(origin)
            if drone:
                return self.book_module.assign_booking(drone, origin, destination, self.username)
            else:
                return "No drone available currently. Please try again later."
        else:
            return message
