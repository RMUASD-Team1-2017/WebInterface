from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver, RabbitMQReceiver_
from EmergencyCommon.models import Drone, DronePosition, DroneMission
import random
import time
import threading
import traceback
import json


class ConsumerTests(TestCase):
    def test_update_drone_location(self):
        print("Testing update_drone_location")
        ids = ['3' , '5', '7']
        data =  {   'current_time' : "2017/05/27_23:11:29",
                    'position' : {'latitude' : 21.315325214, 'longitude' : 22.325252414321, 'altitude' : 30.5},
                    'destination' :  {'latitude' : 25.315325214, 'longitude' : 20.325252414321, 'altitude' : 30.5},
                    'waypoint' : {'latitude' : 51.315325214, 'longitude' : -22.325252414321, 'altitude' : 30.5},
                    'eta' : 127,
                    'state' :  'flying',
                    'mission_id' : 1,
                    'serial' : 1
                }
        loops = 3
        for id_ in ids:
            data['mission_id'] = random.randint(1, 10 ** 10)
            data['serial'] = random.randint(1, 10 ** 10)
            data_str = json.dumps(data)
            # try:
            #     mis = DroneMission.objects.filter(id=data['state']['mission_id'])[0]
            # except:
            #     mis = DroneMission(id = data['state']['mission_id'])
            #     mis.save()
            for i in range(loops):
                rabbit_sender.add_message(exchange='drone',
                              routing_key="drone.status",
                              body=data_str)
        for i in range(30):
            try:
                time.sleep(0.2)
                if(Drone.objects.all().count() < len(ids)): continue
                self.assertEqual(Drone.objects.all().count(), len(ids))

                if(DronePosition.objects.all().count() < len(ids) * loops): continue
                self.assertEqual(DronePosition.objects.all().count(), len(ids) * loops)

                return
            except KeyError:
                continue
        raise KeyError("Something went wrong when creating drone objects.")
