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
    #Test if the drone exists, if not, create it.
    try:
        drone = Drone.objects.filter(serial=_id)[0]
    except:
        drone = Drone(serial = _id)
    #Add drone state to db
    try:
        last_update = make_aware(datetime.datetime.strptime(data['current_time'], '%Y/%m/%d_%H:%M:%S'))
        eta = last_update + datetime.timedelta(seconds = data['ETA'])
        drone.latitude = float(data['position']['latitude'])
        drone.longtitude = float(data['position']['longtitude'])
        drone.goal_latitude = float(data['destination']['goal']['latitude'])
        drone.goal_longtitude = float(data['destination']['goal']['longtitude'])
        drone.waypoint_latitude = float(data['destination']['waypoint']['latitude'])
        drone.waypoint_longtitude = float(data['destination']['waypoint']['longtitude'])
        drone.last_update = last_update
        drone.eta = eta
        drone.state = data['state']
        drone.save()
        position = DronePosition(   drone = drone,
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
