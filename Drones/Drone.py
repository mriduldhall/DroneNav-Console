class Drone:
    def __init__(self, id, location_id, job, user_id, route_id, job_start_time, job_duration, job_finish_time, origin_id, destination_id):
        self.job_finish_time = job_finish_time
        self.destination_id = destination_id
        self.origin_id = origin_id
        self.job_duration = job_duration
        self.job_start_time = job_start_time
        self.route_id = route_id
        self.user_id = user_id
        self.location_id = location_id
        self.job = job
        self.id = id
