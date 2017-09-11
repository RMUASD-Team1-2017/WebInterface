import pika
from threading import RLock, Thread

class RabbitMQSender_():
    global_lock = RLock()
    def __init__(self):
        with self.global_lock:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='location')


    def get_connection(self):
        with self.global_lock:
            return self.connection
    def get_channel(self):
        with self.global_lock:
            return self.channel

    def reconnect(self):
        with self.global_lock:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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



class RabbitMQReciever_(RabbitMQSender_):
    def __init__(self):
        with self.global_lock:
            super().__init__()
            self.channel.queue_declare(queue='hello')

    def start_consuming(self):
        self.consume_thread = Thread(target = self.channel.start_consuming, daemon = True)
        self.consume_thread.start()

    def stop_consuming(self):
        self.channel.basic_cancel()

    def __del__(self):
        self.stop_consuming()
        self.join()

class RabbitMQReciever():
    instance = None
    def __init__(self):
        pass
    @classmethod
    def get_instance(self):
        if RabbitMQReciever.instance is None:
            pass
            RabbitMQReciever.instance = RabbitMQReciever_()
        return RabbitMQReciever.instance


rabbit_sender = RabbitMQSender.get_instance()
rabbit_reciever = RabbitMQReciever.get_instance()
