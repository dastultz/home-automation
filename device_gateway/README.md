# incoming messages
# request state of a specific component:
# to/device_id/component
# to/garage/door
# subscribe to all messages targeted to this device
# to/garage/#

# request state of all components:
# to/garage/*

# set state of a specific component:
# to/device_id/component/set
# to/garage/light/set

# outgoing messages
# report the status of a specific component:
# from/device_id/component
# from/garage/component

https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-for-esp8266

Erase and re-flash
esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
esptool.py --port /dev/tty.SLAB_USBtoUART --baud 115200 write_flash --flash_size=detect 0 ~/Downloads/adafruit-circuitpython-feather_huzzah-3.1.1.bin

ampy:
Commands:
  get    Retrieve a file from the board.
  ls     List contents of a directory on the board.
  mkdir  Create a directory on the board.
  put    Put a file or folder and its contents on the board.
  reset  Perform soft reset/reboot of the board.
  rm     Remove a file from the board.
  rmdir  Forcefully remove a folder and all its children from the board.
  run    Run a script and print its output.

Breakout board pinout

from perspective of USB port pointing down

upper left      upper right
Y7              GND
Y5              GND
Y6              GND
Y3              n/c
Y0              n/c
Y1              5V
Y2              GPIO4
Y4              n/c
