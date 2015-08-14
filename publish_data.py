from __future__ import division
from protobuf.cta_event_pb2 import CTAEvent
import zmq
from time import sleep
import numpy as np
from telescope import LST

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5000")

lst = LST(position_x=0, position_y=0, telescope_id=0)


while True:
    event = CTAEvent()
    event.telescope_id = lst.telescope_id
    # for value in np.random.normal(size=lst.n_pixel):
    data = np.random.normal(size=lst.n_pixel)
    event.data.extend(list(data))
    socket.send('1000 ' + event.SerializeToString())
    # socket.send('1000 Hallo Welt')
    sleep(1/16)
