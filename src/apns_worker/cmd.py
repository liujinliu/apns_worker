#coding=utf-8
from apns_worker.mq import agent
from apns_worker.api import send
import tornado.ioloop
import json
from tornado.options import define, options, parse_command_line

define('cert', default='certfile_fullpath', help='apns cert file')
define('key', default='keyfile_fullpath', help='apns key file')
define('mqhost', default='localhost', help='rabbitmq host ip')
define('mqport', default=5672, help='rabbitmq port')
define('mquser', default='apns', help='user name of rabbitmq')
define('mqpass', default='apns', help='user pass of rabbitmq')
define('mqvhost', default='apns', help='vhost of rabbitmq')
define('mqexchange', default='apns', help='exchange')
define('queuename', default='apns', help='message queue name')
define('routingkey', default='worker.apns', help='routing key')

def consumer(msg):
    msg.ack()
    paras = json.loads(msg.body)
    #print paras
    send.apns_notifiaction_send(
        paras['appname'], paras['content'],
        paras['sound'], paras['badge'],
        paras['token_list'], paras['item'])

def worker_start():
    parse_command_line()
    amqp_agent = agent.AMQPAgent(
                consumer, options.queuename,
                options.routingkey, options.mqhost,
                options.mqport, options.mquser,
                options.mqpass, options.mqvhost,
                options.mqexchange)
    amqp_agent.connect()
    tornado.ioloop.IOLoop.instance().start()


