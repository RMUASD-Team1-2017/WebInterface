from EmergencyRabbitMQ import rabbit_sender
import json

exchange = "drone"
rabbit_sender.add_exchange(exchange, "topic")
def send_mission_request(mission):
    message = json.dumps({"mission_id" : mission.id, "destination" : {'latitude' : mission.call_latitude, 'longitude' : mission.call_longitude}} )

    rabbit_sender.add_message(exchange, "drone.mission_request", message )
