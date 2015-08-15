'''
this script publishes LST events with white noise
using zeromq and protobuf

Usage:
    publish_data.py [options]

Options:
    --ip=<ip>       the ip where the data is published [default: 127.0.0.1]
    --port=<port>   the port where the data is published [default: 5000]
'''
from __future__ import division
from protobuf.cta_event_pb2 import CTAEvent
import zmq
from time import sleep
import numpy as np
from telescope import LST

from docopt import docopt
args = docopt(__doc__)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://{ip}:{port}".format(ip=args['--ip'], port=args['--port']))

lst = LST(position_x=0, position_y=0, telescope_id=0)

try:
    while True:
        event = CTAEvent()
        event.telescope_id = lst.telescope_id
        data = np.random.normal(size=lst.n_pixel)
        event.data.extend(list(data))
        socket.send('1000 ' + event.SerializeToString())
        sleep(1/15)
except (KeyboardInterrupt, SystemExit):
    pass
