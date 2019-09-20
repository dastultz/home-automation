import digitalio
import time
import logger
import gc


class DigitalInSource:

    def __init__(self, pin: int):
        self._in = digitalio.DigitalInOut(pin)
        self._in.switch_to_input(pull=digitalio.Pull.UP)

    @property
    def value(self):
        return self._in.value


class Mux:

    def __init__(self, z_pin, s1_pin, s2_pin, s3_pin):
        self._in = digitalio.DigitalInOut(z_pin)
        self._in.switch_to_input(pull=digitalio.Pull.UP)
        self._s1_pin = digitalio.DigitalInOut(s1_pin)
        self._s1_pin.switch_to_output()
        self._s2_pin = digitalio.DigitalInOut(s2_pin)
        self._s2_pin.switch_to_output()
        self._s3_pin = digitalio.DigitalInOut(s3_pin)
        self._s3_pin.switch_to_output()

    def value(self, s1: bool, s2: bool, s3: bool):
        self._s1_pin.value = s1
        self._s2_pin.value = s2
        self._s3_pin.value = s3
        return self._in.value


class MuxInSource:

    def __init__(self, y_pin: int, mux: Mux):
        self._mux = mux
        self._s1 = y_pin & 0b1 != 0
        self._s2 = y_pin & 0b10 != 0
        self._s3 = y_pin & 0b100 != 0

    @property
    def value(self):
        return self._mux.value(self._s1, self._s2, self._s3)


class Switch:

    def __init__(self, id: str, pin_source):
        self._pin_source = pin_source
        self.id = id
        self.message_bus = None
        self._closed = self._pin_source.value
        self._last_state_change = time.monotonic()  # time in seconds

    def set(self, payload):
        pass

    def service(self):
        pin_state = self._pin_source.value
        changed = False
        if pin_state != self._closed:
            now = time.monotonic()
            if now - self._last_state_change > 0.01:
                self._closed = pin_state
                self._last_state_change = now
                changed = True
        if changed:
            self.do_change()

    def do_change(self):
        self.report_state()

    def report_state(self):
        self.message_bus.publish(self.id, self._closed)


class TemporalMonoNumericKeypad(Switch):

    def __init__(self, id: str, pin_source):
        Switch.__init__(self, id, pin_source)
        self._last_press_time = time.monotonic()  # time in seconds
        self._queue = []
        self._press_count = 0

    def service(self):
        Switch.service(self)
        if len(self._queue) > 0 or self._press_count > 0:
            now = time.monotonic()
            if now - self._last_press_time > 1.0:
                self._queue.append(self._press_count)
                self.report_state()
                self._last_press_time = now
                self._press_count = 0
                self._queue = []

    def do_change(self):
        if self._closed:
            now = time.monotonic()
            span = now - self._last_press_time
            if span > 0.5 and self._press_count > 0:
                self._queue.append(self._press_count)
                self._press_count = 0
            self._press_count += 1
            self._last_press_time = now

    def report_state(self):
        code = ''.join(str(e) for e in self._queue)
        self.message_bus.publish(self.id, code)


class Light:

    def __init__(self, id: str, pin: int):
        self.id = id
        self.message_bus = None
        self._out = digitalio.DigitalInOut(pin)
        self._out.direction = digitalio.Direction.OUTPUT
        self._out.value = False

    def set(self, payload):
        self._out.value = payload
        self.report_state()

    def service(self):
        pass

    def report_state(self):
        self.message_bus.publish(self.id, self._out.value)


class PulseRelay:

    def __init__(self, id: str, pin: int, pulse_time: float = 0.5):
        self.id = id
        self.message_bus = None
        self._last_activated = 0  # time in seconds
        self._pulse_time = pulse_time
        # keep copy of state to avoid reading pin every loop
        self._state = False
        self._out = digitalio.DigitalInOut(pin)
        self._out.direction = digitalio.Direction.OUTPUT
        self._out.value = self._state

    def set(self, payload):
        self._state = payload
        self._out.value = self._state
        if self._state:
            self._last_activated = time.monotonic()
        else:
            self._last_activated = 0
        self.report_state()

    def service(self):
        if self._state:
            now = time.monotonic()
            elapsed = now - self._last_activated
            if elapsed > self._pulse_time:
                self.set(False)

    def report_state(self):
        self.message_bus.publish(self.id, self._state)


class Heartbeat:

    def __init__(self):
        self.id = "SYS-heartbeat"
        self._last_report_time = -100
        self.message_bus = None

    def service(self):
        now = time.monotonic()
        elapsed = now - self._last_report_time
        if elapsed > 10:
            self.report_state()
            self._last_report_time = now

    def report_state(self):
        msg = "%d\t%d" % (time.monotonic(), gc.mem_free())
        self.message_bus.publish(self.id, msg)


class LogManager:

    def __init__(self):
        self.id = "SYS-logman"
        self.message_bus = None

    def service(self):
        pass

    def set(self, payload):
        logger.clear()

    def report_state(self):
        state = logger.get()
        self.message_bus.publish(self.id, state)
