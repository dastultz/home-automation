import board
from components import Switch, Light, PulseRelay, Mux, MuxInSource, TemporalMonoNumericKeypad
from gateway import Gateway


def run():
    gw = Gateway()
    # inputs
    mux = Mux(board.GPIO14, board.GPIO12, board.GPIO15, board.GPIO13)
    gw.add_component(TemporalMonoNumericKeypad("keypad", MuxInSource(0, mux)))  # Y0
    gw.add_component(Switch("beam", MuxInSource(1, mux)))  # Y1
    gw.add_component(Switch("doordown", MuxInSource(2, mux)))  # Y2
    gw.add_component(Switch("doorup", MuxInSource(3, mux)))  # Y3
    gw.add_component(Switch("reardoor", MuxInSource(4, mux)))  # Y4
    gw.add_component(Switch("patiodoor", MuxInSource(5, mux)))  # Y5
    gw.add_component(Switch("frontdoor", MuxInSource(6, mux)))  # Y6
    gw.add_component(Switch("Y7", MuxInSource(7, mux)))  # Y7
    # outputs
    gw.add_component(Light("light", board.GPIO4))
    gw.add_component(PulseRelay("lift", board.GPIO5))

    gw.run()


if __name__ == '__main__':
    run()
