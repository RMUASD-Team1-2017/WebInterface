from EmergencyRabbitMQ import rabbit_sender
import json
exchange = 'drone' #str(random.randint(1, 10**20))
queue = rabbit_sender.get_channel().queue_declare(exclusive = True).method.queue

def send_mission_request(mission):
    message = json.dumps({'latitude' : mission.call_latitude, 'longtitude' : mission.call_longtitude})

    rabbit_sender.get_channel().basic_publish(exchange=exchange,
                  routing_key="drone.{}.mission_request".format(mission.id),
                  body=message)
