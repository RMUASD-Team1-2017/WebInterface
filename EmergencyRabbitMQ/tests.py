from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver, RabbitMQReceiver_
from EmergencyCommon.models import Drone, DronePosition
import random
import time
import threading
import traceback
import json

class RabbitMQTests(TestCase):
#Simple test to see if we can retrieve the webpages
    recieved = {}
    lock = threading.RLock()
    def consumer_callback(self, ch, method, properties, body):
        with self.lock:
            try:
                self.assertEqual(self.recieved[method.exchange][method.routing_key]["body"], body.decode('utf-8'))
                self.recieved[method.exchange][method.routing_key]["count"] += 1
            except KeyError:
                if method.exchange in self.recieved:
                    self.recieved[method.exchange][method.routing_key] = {"body" : body.decode('utf-8'), "count" : 1}
                else:
                    self.recieved[method.exchange] = {}
                    self.recieved[method.exchange][method.routing_key] = {"body" : body.decode('utf-8'), "count" : 1}
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def test_workqueue(self):
        print("Testing RabbitMQ workqueue")
        rabbit_receiver.stop_consuming()
        queue = rabbit_sender.get_channel().queue_declare().method.queue
        rabbit_receiver.get_channel().basic_consume(self.consumer_callback,
                              queue=queue,
                              no_ack=False)

        rabbit_receiver.start_consuming()
        message = str(random.randint(1, 10**20 ))
        rabbit_sender.get_channel().basic_publish(exchange='',
                  routing_key=queue,
                  body= message)

        for i in range(10):
            try:
                time.sleep(0.2)
                self.assertEqual(self.recieved[''][queue]["body"], message)
                return
            except KeyError:
                continue

        raise KeyError("Never recieved message from server")

    def test_fanout(self):
        print("Testing RabbitMQ fanout")
        reciever_count = 2
        recievers = [RabbitMQReceiver_() for x in range(reciever_count)]
        exchange = str(random.randint(1, 10**20))
        message = str(random.randint(1, 10**20))

        rabbit_sender.get_channel().exchange_declare(exchange=exchange,
                                                    type='fanout')

        for receiver in recievers:
            queue = receiver.get_channel().queue_declare(exclusive = True).method.queue
            receiver.get_channel().queue_bind(exchange=exchange,
                                                    queue=queue)
            receiver.get_channel().basic_consume(self.consumer_callback,
                                  queue=queue)
            receiver.start_consuming()


        time.sleep(.1)
        rabbit_sender.get_channel().basic_publish(exchange=exchange,
                              routing_key='',
                              body=message)

        for i in range(30):
            try:
                time.sleep(0.2)
                if(self.recieved[exchange]['']['count'] < reciever_count): continue
                self.assertEqual(self.recieved[exchange]['']['count'], reciever_count)
                return
            except KeyError:
                continue
        raise KeyError("Did not receive 3 messages from broker as expected")

    def test_topics(self):
        print("Testing RabbitMQ topics")

        reciever_count = 2
        topics = ["info.good", "info.bad", "info.#", "warning.good", "warning.bad", "warning.#", "error.good", "error.bad", "error.#"]
        recievers = [(RabbitMQReceiver_(), topics[x])  for x in range(len(topics))]

        exchange = str(random.randint(1, 10**20))
        message = str(random.randint(1, 10**20))

        rabbit_sender.get_channel().exchange_declare(exchange=exchange,
                                                    type='topic')

        for receiver, routing_key in recievers:
            queue = receiver.get_channel().queue_declare(exclusive = True).method.queue
            receiver.get_channel().queue_bind(exchange=exchange,
                                                    queue=queue,
                                                    routing_key = routing_key)
            receiver.get_channel().basic_consume(self.consumer_callback,
                                  queue=queue)
            receiver.start_consuming()

        time.sleep(0.1)
        for key in ["info.bad", "info.good", "warning.bad", "error.bad", "error.good"]:
            rabbit_sender.get_channel().basic_publish(exchange=exchange,
                          routing_key=key,
                          body=message)

        for i in range(30):
            try:
                time.sleep(0.2)
                if(self.recieved[exchange]['info.bad']['count'] < 2): continue
                self.assertEqual(self.recieved[exchange]['info.bad']['count'], 2)

                if(self.recieved[exchange]['info.good']['count'] < 2): continue
                self.assertEqual(self.recieved[exchange]['info.good']['count'], 2)

                if(self.recieved[exchange]['warning.bad']['count'] < 2): continue
                self.assertEqual(self.recieved[exchange]['warning.bad']['count'], 2)

                if(self.recieved[exchange]['error.bad']['count'] < 2): continue
                self.assertEqual(self.recieved[exchange]['error.bad']['count'], 2)

                if(self.recieved[exchange]['error.good']['count'] < 2): continue
                self.assertEqual(self.recieved[exchange]['error.good']['count'], 2)

                return
            except KeyError:
                continue
        raise KeyError("Did not receive messages from broker as expected")


class ConsumerTests(TestCase):
    def test_update_drone_location(self):
        print("Testing update_drone_location")
        ids = ['3' , '5', '7']
        data =  {   'current_time' : "2017/05/27_23:11:29",
                    'position' : {'latitude' : 21.315325214, 'longtitude' : 22.325252414321},
                    'destination' : { 'goal' : {'latitude' : 25.315325214, 'longtitude' : 20.325252414321}, 'waypoint' : {'latitude' : 51.315325214, 'longtitude' : -22.325252414321}},
                    'ETA' : 127,
                    'state' : {'mission_state' : 'flying', 'mission_id' : None }
                }
        loops = 3
        for id_ in ids:
            data['state']['mission_id'] = random.randint(1, 10 ** 10)
            data_str = json.dumps(data)
            for i in range(loops):
                rabbit_sender.get_channel().basic_publish(exchange='drone',
                              routing_key="drone." + str(id_) + ".status",
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
