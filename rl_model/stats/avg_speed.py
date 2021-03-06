from simulation import SimulationComponent
import numpy as np
import traci

class OverallAverageSpeedRecorder(SimulationComponent):
    def __init__(self, simulation):
        self._speeds = []
        self._simulation = simulation

    def tick(self):
        avg = 0
        for veh_id in traci.simulation.getDepartedIDList():
            traci.vehicle.subscribe(veh_id, [traci.constants.VAR_SPEED])
        velocities = traci.vehicle.getSubscriptionResults()
        for i in velocities.values():
            avg += i[traci.constants.VAR_SPEED]
        vehicle_count = traci.vehicle.getIDCount()
        if vehicle_count != 0:
            avg/= vehicle_count
        self._speeds.append(avg)


    def post_run(self):
        self._simulation.results["avg_speed"] = np.asarray(self._speeds)