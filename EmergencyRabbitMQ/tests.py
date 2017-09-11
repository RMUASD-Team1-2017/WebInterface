from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver, RabbitMQReceiver_
import random
import time
import threading
import traceback
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
        reciever_count = 5
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

        reciever_count = 5
        topics = ["info.good", "info.bad", "info.#", "warning.good", "warning.bad", "warning.#", "error.good", "error.bad", "error.#"]
        recievers = [(RabbitMQReceiver_(), topics[x])  for x in range(len(topics))]

        exchange = 'topic_logs' #str(random.randint(1, 10**20))
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

        time.sleep(1)
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
