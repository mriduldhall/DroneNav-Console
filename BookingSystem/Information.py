from HelperLibrary.StorageFunctions import StorageFunctions


class Information:
    def __init__(self, username):
        self.username = username

    def execute(self):
        user_data = StorageFunctions("users").retrieve(["username"], [self.username])
        user_id = (user_data[0])[0]
        drones_data = StorageFunctions("drones").retrieve(["user_id"], [user_id])
        if not drones_data:
            print("You have not booked any drones")
        else:
            print("You have booked:")
            counter = 1
            for booked_data in drones_data:
                origin_data = StorageFunctions("locations").retrieve(["id"], [booked_data[7]])
                origin = (origin_data[0])[1]
                destination_data = StorageFunctions("locations").retrieve(["id"], [booked_data[8]])
                destination = (destination_data[0])[1]
                print(counter, ": Drone number - ", booked_data[0], ", from ", origin, " to ", destination, sep='')
                counter += 1
