import sys
import time

import network
import logger

from config import config

wifi = None


def connect():
    global wifi
    # turn off the WiFi Access Point
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    # connect the device to the WiFi network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(config['ssid'], config['password'])

    # wait until the device is connected to the WiFi network
    max_attempts = 20
    attempt_count = 0
    while not wifi.isconnected() and attempt_count < max_attempts:
        attempt_count += 1
        time.sleep(1)

    if attempt_count == max_attempts:
        logger.log("E1")
        sys.exit()

    logger.log("E2 {}".format(attempt_count))
