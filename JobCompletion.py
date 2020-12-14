import time
from datetime import datetime

from HelperLibrary.StorageFunctions import StorageFunctions

if __name__ == '__main__':
    while True:
        drones_list = StorageFunctions("drones").retrieve(["job"], [True])
        if drones_list:
            for drone in drones_list:
                job_finish_time = drone[7]
                if datetime.now() >= job_finish_time:
                    StorageFunctions("drones").update(["location_id", "job", "user_id", "route_id", "job_start_time", "job_duration", "job_finish_time", "origin_id", "destination_id"], [drone[9], False, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'], drone[0])
        time.sleep(120)
