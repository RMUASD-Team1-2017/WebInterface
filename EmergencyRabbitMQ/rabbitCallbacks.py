from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver
import json
from EmergencyCommon.models import *
import datetime
import traceback
#define callbacks
from django.utils.timezone import make_aware
def update_drone_location_callback(ch, method, properties, body):
    _id = method.routing_key.split('.')[1]
    data = json.loads(body.decode('utf-8'))
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
    mission_id = data['state']['mission_id']
    if data['state']['mission_id']:
        try:
            mission = DroneMission.objects.filter(id = mission_id)[0]
        except IndexError:
            mission = DroneMission(the_drone = drone, id = mission_id )
            if mission.accepted is False:
                mission.start = last_update
                mission.accepted = True
        mission.goal_latitude = float(data['destination']['goal']['latitude'])
        mission.goal_longtitude = float(data['destination']['goal']['longtitude'])
        mission.waypoint_latitude = float(data['destination']['waypoint']['latitude'])
        mission.waypoint_longtitude = float(data['destination']['waypoint']['longtitude'])
        mission.eta = eta
        mission.last_update = last_update
        mission.save()
    #Add drone state to db
    try:
        drone.latitude = float(data['position']['latitude'])
        drone.longtitude = float(data['position']['longtitude'])
        drone.last_update = last_update
        drone.state = data['state']['mission_state']
        drone.save()
        drone.current_mission = mission
        position = DronePosition(   the_drone = drone,
                                    latitude = float(data['position']['latitude']),
                                    longtitude = float(data['position']['longtitude']),
                                    time = last_update
                                )
        position.save()
    except:
        print("Error in update drone location")
        traceback.print_exc()
    #Always ACK for now?
    ch.basic_ack(delivery_tag = method.delivery_tag)


def register_callbacks():
    ##Setup queues, exchanges and callbacks
    exchange = 'drone'
    rabbit_receiver.get_channel().exchange_declare(exchange=exchange,
                                                type='topic')

    queue = rabbit_receiver.get_channel().queue_declare(exclusive = True).method.queue

    rabbit_receiver.get_channel().queue_bind(exchange=exchange,
                                      queue=queue,
                                      routing_key = "drone.*.status")

    rabbit_receiver.get_channel().basic_consume(update_drone_location_callback,
                                        queue=queue)