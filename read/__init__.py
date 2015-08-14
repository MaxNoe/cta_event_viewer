from threading import Thread
import zmq
from protobuf.cta_event_pb2 import CTAEvent


class ReadProtoBuf(Thread, object):
    '''reads cta data from protobuf and pushes the data into the tk window '''

    def __init__(self, ip, port, queue, stop_event):
        Thread.__init__(self)
        self.stop_event = stop_event
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://{ip}:{port}'.format(ip=ip, port=port))
        self.socket.setsockopt(zmq.SUBSCRIBE, '1000')
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.queue = queue

    def run(self):
        while not self.stop_event.is_set():
            self.read()

    def read(self):
        mesg = self.poller.poll(500)
        if mesg:
            event = CTAEvent()
            rec = self.socket.recv()
            binary_data = rec[5:]
            event.ParseFromString(binary_data)
            self.queue.append(event)
