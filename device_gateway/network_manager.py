import time

import network

import logger
from config import config

_wifi = None


def connect(reconnecting=False):
    global _wifi
    if not reconnecting:
        # turn off the WiFi Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

    # connect the device to the WiFi network
    _wifi = network.WLAN(network.STA_IF)
    _wifi.active(True)
    try:
        _wifi.connect(config['ssid'], config['password'])

        # wait until the device is connected to the WiFi network
        while not _wifi.isconnected():
            time.sleep(1)
        logger.log("E1")

    except OSError as exc:
        logger.log("E1b %r" % exc)
        reconnect()

    logger.log("E2")


def reconnect():
    global _wifi
    if _wifi is None or not _wifi.isconnected():
        logger.log("E5")
        connect(reconnecting=True)
