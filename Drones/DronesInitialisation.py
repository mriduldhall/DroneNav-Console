from HelperLibrary.StorageFunctions import StorageFunctions

for _ in range(0, 22):
    StorageFunctions("drones").append("(location_id, job)", [str(1), False])

for _ in range(0, 8):
    StorageFunctions("drones").append("(location_id, job)", [str(2), False])

for _ in range(0, 11):
    StorageFunctions("drones").append("(location_id, job)", [str(3), False])

for _ in range(0, 19):
    StorageFunctions("drones").append("(location_id, job)", [str(4), False])

for _ in range(0, 15):
    StorageFunctions("drones").append("(location_id, job)", [str(5), False])

for _ in range(0, 18):
    StorageFunctions("drones").append("(location_id, job)", [str(6), False])

for _ in range(0, 7):
    StorageFunctions("drones").append("(location_id, job)", [str(7), False])
