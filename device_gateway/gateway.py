import time

import network_startup
from components import Heartbeat, LogManager
from message_bus import MessageBus
import logger


class Gateway:

    def __init__(self):
        self._message_bus = MessageBus(self._on_message)
        self._components = []
        self._component_dict = {}

    def add_component(self, component):
        self._components.append(component)
        self._component_dict[component.id] = component
        component.message_bus = self._message_bus

    def run(self):
        self.add_component(Heartbeat())
        self.add_component(LogManager())
        network_startup.connect()
        self._message_bus.connect()

        # report status of all components
        self._report_all()

        print("A1")
        try:
            while True:
                self._message_bus.service()
                for component in self._components:
                    component.service()
                    time.sleep(0.01)
        except Exception as exc:
            logger.log("E6 %s" % exc)
            # todo: reboot? https://circuitpython.readthedocs.io/en/latest/shared-bindings/supervisor/__init__.html#supervisor.reload

    def _on_message(self, component_id, payload):
        report_all = component_id == "*"  # report only, maybe should be ../$SYS/report-all
        is_set = payload is not None

        if report_all:
            self._report_all()
        elif is_set:
            component = self._component_dict[component_id]
            component.set(payload)
        else:
            component = self._component_dict[component_id]
            component.report_state()

    def _report_all(self):
        for component in self._components:
            component.report_state()

