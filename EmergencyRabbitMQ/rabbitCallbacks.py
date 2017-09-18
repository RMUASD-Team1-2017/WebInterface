import json
import datetime
import traceback
#define callbacks
from django.utils.timezone import make_aware

def update_drone_location_callback(ch, method, properties, body):
    from EmergencyCommon.models import Drone, DroneMission, DronePosition

    data = json.loads(body.decode('utf-8'))
    print(body)
    last_update = make_aware(datetime.datetime.strptime(data['current_time'], '%Y/%m/%d_%H:%M:%S'))
    eta = None
    if data['ETA']: eta = last_update + datetime.timedelta(seconds = data['ETA'])

    #Test if the drone exists, if not, create it.
    try:
        drone = Drone.objects.filter(serial=_id)[0]
    except IndexError:
        drone = Drone(serial = _id)
    drone.save()
    #Test if mission exists, if not, create if
    mission = None
    mission_id = data["mission_id"]
    if mission_id:
        try:
            mission = DroneMission.objects.filter(id = mission_id)[0]
            mission.the_drone = drone
            mission.goal_latitude = float(data['destination']['goal']['latitude'])
            mission.goal_longitude = float(data['destination']['goal']['longitude'])
            mission.waypoint_latitude = float(data['destination']['waypoint']['latitude'])
            mission.waypoint_longitude = float(data['destination']['waypoint']['longitude'])
            mission.eta = eta
            mission.last_update = last_update
            mission.save()
        except IndexError:
            print("Recieved message about mission {}, which does not seem to exist!".format(mission_id))

    #Add drone state to db
    try:
        drone.latitude = float(data['position']['latitude'])
        drone.longitude = float(data['position']['longitude'])
        drone.last_update = last_update
        drone.state = data['state']['mission_state']
        drone.save()
        drone.current_mission = mission
        position = DronePosition(   the_drone = drone,
                                    latitude = float(data['position']['latitude']),
                                    longitude = float(data['position']['longitude']),
                                    time = last_update
                                )
        position.save()
    except:
        print("Error in update drone location")
        traceback.print_exc()
    #Always ACK for now?
    ch.basic_ack(delivery_tag = method.delivery_tag)
