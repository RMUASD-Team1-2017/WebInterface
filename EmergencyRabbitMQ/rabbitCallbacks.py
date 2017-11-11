import json
import datetime
import traceback
#define callbacks
from django.utils.timezone import make_aware

def oes_location_callback(ch, method, properties, body):
    try:
        from EmergencyCommon.models import Drone, DroneMission, DronePosition
        data = json.loads(body.decode('utf-8'))
        print(data)
        last_update = make_aware(datetime.datetime.strptime(data['time'], '%Y/%m/%d_%H:%M:%S'))
        #Test if the drone exists, if not, create it.
        serial = method.routing_key.split(".")[-1]
        print(serial)
        try:
            drone = Drone.objects.filter(serial=serial)[0]
        except IndexError:
            drone = Drone(serial=serial)
        drone.oes_latitude = data["location"]["lat"]
        drone.oes_longitude = data["location"]["lon"]
        drone.oes_altitude = data["location"]["alt"]
        drone.save()
    except:
        print("Error in update drone location")
        traceback.print_exc()

def update_drone_location_callback(ch, method, properties, body):
    try:
        from EmergencyCommon.models import Drone, DroneMission, DronePosition
        data = json.loads(body.decode('utf-8'))
        last_update = make_aware(datetime.datetime.strptime(data['current_time'], '%Y/%m/%d_%H:%M:%S'))
        eta = None
        if data['eta']: eta = last_update + datetime.timedelta(seconds = data['eta'])

        #Test if the drone exists, if not, create it.
        try:
            drone = Drone.objects.filter(serial=data["serial"])[0]
        except IndexError:
            drone = Drone(serial=data["serial"])
        drone.save()
        #Test if mission exists, if not, create if
        mission = None
        mission_id = data["mission_id"]
        if mission_id:
            try:
                mission = DroneMission.objects.filter(id = mission_id)[0]
                mission.the_drone = drone
                mission.goal_latitude = float(data['destination']['latitude'])
                mission.goal_longitude = float(data['destination']['longitude'])
                mission.waypoint_latitude = float(data['waypoint']['latitude'])
                mission.waypoint_longitude = float(data['waypoint']['longitude'])
                mission.eta = eta
                mission.last_update = last_update
                mission.save()
            except IndexError:
                print("Recieved message about mission {}, which does not seem to exist!".format(mission_id))

        #Add drone state to db
        try:
            drone.latitude = float(data['position']['latitude'])
            drone.longitude = float(data['position']['longitude'])
            drone.altitude = float(data['position']['altitude'])
            drone.last_update = last_update
            drone.state = data['state']
            drone.save()
            drone.current_mission = mission
            position = DronePosition(   the_drone = drone,
                                        latitude = float(data['position']['latitude']),
                                        longitude = float(data['position']['longitude']),
                                        altitude = float(data['position']['altitude']),
                                        time = last_update
                                    )
            position.save()
        except:
            print("Error in update drone location")
            traceback.print_exc()
    except:
        print("Error in update drone location")
        traceback.print_exc()
    #Always ACK for now
    ch.basic_ack(delivery_tag = method.delivery_tag)
