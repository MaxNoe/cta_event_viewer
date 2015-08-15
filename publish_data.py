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
from scipy.stats import multivariate_normal

from docopt import docopt


def rotate_angle(mat, angle):
    mat = np.matrix(mat)
    rot = np.matrix([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]])

    return rot * mat * rot.T


def random_shower(telescope):
    px = telescope.pixel_x
    py = telescope.pixel_y
    coords = np.vstack([px, py])
    radius = max(np.sqrt(px**2 + py**2))
    mean = np.random.uniform(-0.8*radius, 0.8*radius, 2)
    length = np.random.uniform(0.05, 0.1)

    width = np.random.uniform(0.05, 0.75) * length

    cov = [[width, 0], [0, length]]
    angle = np.random.uniform(0, 2*np.pi)
    cov = rotate_angle(cov, angle)
    size = np.random.poisson(width * length * np.random.normal(5e5, 1e5))

    photon_expectance = size * telescope.pixel_size * multivariate_normal.pdf(
        coords.T, mean, cov
    )

    photons = np.random.poisson(photon_expectance).astype(float)
    photons += np.random.normal(0.0, 1.0, telescope.n_pixel)

    return photons

if __name__ == '__main__':
    try:
        args = docopt(__doc__)

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(
            "tcp://{ip}:{port}".format(ip=args['--ip'], port=args['--port'])
        )

        lst = LST(position_x=0, position_y=0, telescope_id=0)

        while True:
            event = CTAEvent()
            event.telescope_id = lst.telescope_id
            data = random_shower(lst)
            event.data.extend(list(data))
            socket.send('1000 ' + event.SerializeToString())
            sleep(1/20)
    except (KeyboardInterrupt, SystemExit):
        pass
