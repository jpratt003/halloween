import socketio


class Honk:
    def __init__(self, server="http://honk.monkey.rutherford.patternlabs.tech"):
        self.sio = socketio.Client()
        self.sio.connect(server)

    def honk(self, time: float = 1.0):
        self.sio.emit("nootnoot", {"duration": time})
