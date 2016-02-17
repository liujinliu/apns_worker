#coding=utf-8
import logging
import time
from tornado.ioloop import IOLoop
from stormed import Connection, Message
from stormed.frame import status as stormed_status

LOG = logging.getLogger(__name__)
class AMQPAgent(object):

    def __init__(self, consumer, queue_name, 
                 routing_key,
                 host='localhost',
                 port=5672, username='apns', 
                 password='apns',
                 vhost='apns',
                 exchange='apns'):
        self._consumer = consumer
        self.exchange = exchange
        self.queue_name = queue_name
        self.routing_key = routing_key
        self._connection = Connection(host=host,
                          port=port, username=username,
                          password=password,vhost=vhost,
                          heartbeat=0)
        self._connection.on_disconnect = self._on_disconnect

    def connect(self):
        """Make Connection
        """
        LOG.warn('Connecting...')
        self._connection.connect(self._on_connect)

    def _on_connect(self):
        def _queue_callback(qinfo):
            self._channel.queue_bind(
                    exchange=self.exchange,
                    queue=qinfo.queue,
                    routing_key=self.routing_key
                    )
            self._channel.consume(qinfo.queue,
                    self._consumer,
                    no_ack=False)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
                exchange=self.exchange,
                type='direct',
                durable='true'
                )
        self._channel.queue_declare(
                queue=self.queue_name,
                callback=_queue_callback,
                durable='true',
                )

    def _on_disconnect(self):
        """Handle And Process When Disconnect
        """
        def _callback():
            self._connection.reset()
            self.connect()

        LOG.warn('AMQ CONNECTION IS %s', self._connection.status)

        if self._connection.status != stormed_status.CLOSED:
            IOLoop.instance().add_timeout(
                time.time() + 2, _callback)
