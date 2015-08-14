from telescope import LST
from windows import TelescopeEventView
import Tkinter as tk
from itertools import cycle
import numpy as np
from read import ReadProtoBuf
from threading import Event

from collections import deque

queue = deque(maxlen=100)
stop_event = Event()


def check_queue():
    if len(queue) > 0:
        root.event_generate('<<new_event>>')
    root.after(10, check_queue)


def handle_new_event(event):
    viewer = next(viewers)
    event = queue.popleft()
    viewer.data = np.array(event.data)


lst = LST(position_x=0, position_y=0, telescope_id=0)

root = tk.Tk()

reader = ReadProtoBuf(
    '127.0.0.1',
    5000,
    queue,
    stop_event,
)


top = tk.Frame(root)
bottom = tk.Frame(root)

viewer1 = TelescopeEventView(top, lst)
viewer2 = TelescopeEventView(top, lst)
viewer3 = TelescopeEventView(top, lst)
viewer4 = TelescopeEventView(bottom, lst)
viewer5 = TelescopeEventView(bottom, lst)
viewer6 = TelescopeEventView(bottom, lst)

viewers = cycle(
    [viewer1, viewer2, viewer3, viewer4, viewer5, viewer6]
)

viewer1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer4.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer5.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer6.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

root.bind('<<new_event>>', handle_new_event)
top.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
bottom.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)


if __name__ == '__main__':
    try:
        reader.start()
        root.after(1, check_queue)
        root.mainloop()
    except (SystemExit, KeyboardInterrupt):
        pass
    stop_event.set()
