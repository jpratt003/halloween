import json

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.on("nootnoot")
def noot(sid, data):
    print("noot ", data)
    sio.emit(
        "nootnoot",
        data,
    )


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
