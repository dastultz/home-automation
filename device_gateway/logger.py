import time
import gc

LOG_FILE = "log.txt"


def log(msg):
    with open(LOG_FILE, "a") as file:
        file.write("%d\t%d\t%s" % (time.monotonic(), gc.mem_free(), msg))
        file.write("\n")


def get():
    with open(LOG_FILE, "r") as file:
        return file.readlines()


def clear():
    with open(LOG_FILE, "w") as file:
        file.write("")

