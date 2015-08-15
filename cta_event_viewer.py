'''
A viewer for cta events, currently only LSTs are supported

Usage:
    cta_event_viewer.py [options]

Options:
    --ip=<ip>       the ip to listen to [default: 127.0.0.1]
    --port=<port>   the port to listen to [default: 5000]
    --rows=<rows>   number of rows of telescope views [default: 2]
    --cols=<cols>   number of columns of telescope views [default: 2]
'''
from telescope import LST
from windows import TelescopeEventView
import Tkinter as tk
from itertools import cycle
import numpy as np
from read import ReadProtoBuf
from threading import Event

from collections import deque
from docopt import docopt

args = docopt(__doc__)

queue = deque(maxlen=100)
stop_event = Event()


def check_queue():
    if len(queue) > 0:
        root.event_generate('<<new_event>>')
    root.after(10, check_queue)


def handle_new_event(event):
    viewer = next(viewers)
    event = queue.popleft()
    print(len(queue))
    viewer.data = np.array(event.data)


root = tk.Tk()

reader = ReadProtoBuf(
    args['--ip'],
    args['--port'],
    queue,
    stop_event,
)

viewers = []
for i in range(int(args['--rows'])):
    root.rowconfigure(i, weight=1)
    for j in range(int(args['--cols'])):
        root.columnconfigure(j, weight=1)
        viewer = TelescopeEventView(root, LST, cmap='hot')
        viewer.grid(row=i, column=j, sticky='nswe')
        viewers.append(viewer)

viewers = cycle(viewers)
root.bind('<<new_event>>', handle_new_event)


if __name__ == '__main__':
    try:
        reader.start()
        root.after(1, check_queue)
        root.mainloop()
    except (SystemExit, KeyboardInterrupt):
        pass
    stop_event.set()
