import time
from . import simple
import logger


class MQTTClient(simple.MQTTClient):

    DELAY = 2
    DEBUG = True

    def delay(self, i):
        time.sleep(self.DELAY)

    def log(self, in_reconnect, e):
        if self.DEBUG:
            if in_reconnect:
                logger.log("E3 %r" % e)
            else:
                logger.log("E4 %r" % e)

    def reconnect(self):
        i = 0
        while 1:
            try:
                return super().connect(False)
            except OSError as e:
                self.log(True, e)
                i += 1
                self.delay(i)

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def wait_msg(self):
        while 1:
            try:
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()
