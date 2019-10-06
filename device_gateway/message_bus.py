import time

from umqtt.robust import MQTTClient

import logger
from config import config


class MessageBus:

    def __init__(self, on_message_handler):
        self._on_message_handler = on_message_handler
        self._device_id = config["device_id"]
        self._client = MQTTClient(client_id=self._device_id,
                                  server=config["broker"],
                                  ssl=False)
        self._client.set_message_received_handler(self._on_message)
        self._client.set_connected_handler(self._on_connected)

    def connect(self):
        connected = False
        while not connected:
            try:
                self._client.connect()
                connected = True
            except Exception as exc:
                logger.log("E9 %r" % exc)
                time.sleep(0.5)

    # The callback for when MQTT client has connected
    def _on_connected(self):
        self._client.subscribe("to/{}/#".format(self._device_id))

    def publish(self, component_id, payload):
        payload = str(payload)
        self._client.publish("from/{}/{}".format(self._device_id, component_id), payload)

    def service(self):
        self._client.check_msg()

    # The callback for when a PUBLISH message is received from the server.
    def _on_message(self, topic, payload):
        try:
            topic = str(topic, "ascii")
            payload = self._coerce_payload(str(payload, "ascii"))

            parts = topic.split("/")
            component_id = parts[2]
            is_set = True if len(parts) == 4 and parts[3] == "set" else False
            payload = payload if is_set else None
            self._on_message_handler(component_id, payload)

        except Exception as exc:
            logger.log("E8 %s" %exc)

    @staticmethod
    def _coerce_payload(payload: str):
        bool_test = payload.lower()
        if bool_test == "true":
            payload = True
        elif bool_test == "false":
            payload = False
        return payload
