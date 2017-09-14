from EmergencyRabbitMQ import rabbit_sender
import json

exchange = "drone"
rabbit_sender.add_exchange(exchange, "topic")
def send_mission_request(mission):
    message = json.dumps({'latitude' : mission.call_latitude, 'longtitude' : mission.call_longtitude})

    rabbit_sender.add_message(exchange, "drone.{}.mission_request".format(mission.id), message )
