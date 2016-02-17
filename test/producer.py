#coding=utf-8
import logging
import sys
from tornado.ioloop import IOLoop
from stormed import Connection, Message
import json

mqhost = 'localhost'
mqvhost = 'apns'
mquser = 'apns'
mqpass = 'apns'
queuename = 'apns'
exchange = 'apns'
routing_key = 'worker.apns'
durable = True

def on_connect():
    ch = conn.channel()
    ch.queue_declare(queue=queuename, durable=durable)
    for i in range(10):
        dev_list = [('123456789%d' %i)]#token value of target device
        notification = {'content':'test push message'}
        para_notify = dict(appname='testapp', content=u'测试，请忽略',
                       sound='default', badge=0,token_list=dev_list,
                       item=notification)
        # delivery_mode=2 makes message persistent
        msg = Message(json.dumps(para_notify), delivery_mode=2)
        ch.publish(msg, exchange=exchange, routing_key=routing_key)
    conn.close(callback=done)
def done():
    print "message publish finish "
    io_loop.stop()
logging.basicConfig()
conn = Connection(host=mqhost, vhost=mqvhost,
                  username=mquser, password=mqpass)
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
