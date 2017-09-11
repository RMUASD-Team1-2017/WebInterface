import pika
from threading import RLock, Thread
from django.conf import settings
def dummy_timeout():
    pass

class RabbitMQSender_():
    def __init__(self):
        self.global_lock = RLock()
        with self.global_lock:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_BROKER))
            self.channel = self.connection.channel()


    def get_connection(self):
        with self.global_lock:
            return self.connection
    def get_channel(self):
        with self.global_lock:
            return self.channel

    def reconnect(self):
        with self.global_lock:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_BROKER))
            self.channel = self.connection.channel()

    def __del__(self):
        with self.global_lock:
            self.connection.close()

class RabbitMQSender():
    instance = None
    def __init__(self):
        pass
    @classmethod
    def get_instance(self):
        if RabbitMQSender.instance is None:
            pass
            RabbitMQSender.instance = RabbitMQSender_()
        return RabbitMQSender.instance



class RabbitMQReceiver_(RabbitMQSender_):
    def __init__(self):
        super().__init__()
        self.consume_thread = None

    def start_consuming(self):
        self.consume_thread = Thread(target = self.channel.start_consuming, daemon = True)
        self.consume_thread.start()

    def stop_consuming(self):
        self.connection.add_timeout(0.2, dummy_timeout)
        self.channel.stop_consuming()
        if self.consume_thread:
            self.consume_thread.join()

    def __del__(self):
        self.stop_consuming()


class RabbitMQReceiver():
    instance = None
    def __init__(self):
        pass
    @classmethod
    def get_instance(self):
        if RabbitMQReceiver.instance is None:
            pass
            RabbitMQReceiver.instance = RabbitMQReceiver_()
        return RabbitMQReceiver.instance


rabbit_sender = RabbitMQSender.get_instance()
rabbit_receiver = RabbitMQReceiver.get_instance()
