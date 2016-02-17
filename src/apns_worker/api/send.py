#coding=utf-8
from apns import APNs, Payload
import logging
import time
from tornado.options import options

LOG = logging.getLogger(__name__)

class ApnsPushHandler(object):
    def __init__(self, appname, content, sound, badge,
                 token_list, notification):
        self.error_responses = []
        self.error_tokens = []
        self.status = 'OK'
        self.num_send = 0
        self.num_error = 0
        self.token_list = token_list

        self.payload = Payload(alert=content,
                          sound=sound,
                          badge=badge,
                          custom=notification)
        self.appname = appname
        self.conn = APNs(use_sandbox=False,
                         cert_file=options.cert,
                         key_file=options.key)
        self.conn.gateway_server.connect(self.on_connected)
        return

    def on_connected(self):
        self.conn.gateway_server.receive_response(self.on_response)

    def on_success(self):
        print "sucess...."

    def on_response(self, status, seq):
        print ("sent push message to APNS "
               "gateway error status %s seq %s" 
               % (status, seq))
        self.error_responses.append(sep)

    def payload_token_renew(self,token_list, content,
                            sound, badge, notification):
        self.token_list = token_list
        self.payload = Payload(alert=content,
                          sound=sound,
                          badge=badge,
                          custom=notification)

    def send_notification(self, ident_offset=0):
        expiry = time.time() + 86400
        for ident, token in enumerate(self.token_list):
            self.conn.gateway_server.send_notification(
                ident+ident_offset, expiry, token,
                self.payload, self.on_success)
            self.num_send += 1

    def finish_status(self):
        return dict(status=self.status,
                num_error=len(self.error_responses),
                num_send=len(self.token_list))

def apns_notifiaction_send(appname, content, sound, badge,
                           token_list, item=None):
    if None == item or None == token_list:
        return dict(status='NA', error_tokens=[],num_error=0,num_send=0)

    ios_push_handler = ApnsPushHandler(appname, content, sound, badge,\
                                       token_list, item)
    ios_push_handler.send_notification()
    return ios_push_handler.finish_status()

def apns_notifiaction_send_multi(appname, content_list,
                             token_list, item_list):
    if None == item_list or None == token_list or \
       len(token_list) != len(item_list) or \
       len(content_list) != len(item_list) or \
       len(token_list)+len(item_list) == 0:
        return dict(status='NA', error_tokens=[],num_error=0,num_send=0)
    sound = 'default'
    badge = 1
    ios_push_handler = ApnsPushHandler(appname,content_list[0], sound, badge,
                                       token_list[0], item_list[0])
    _offset = 0
    for i in range(len(token_list)):
        tokens = token_list[i]
        item = item_list[i]
        content = content_list[i]
        ios_push_handler.payload_token_renew(tokens,content, sound, 
                                             badge, item) 
        ios_push_handler.send_notification(_offset)
        _offset += len(tokens)
    return dict(num_send=_offset, num_error=0)

