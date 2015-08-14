from telescope import LST
from windows import TelescopeEventView
import tkinter as tk
from itertools import cycle
import numpy as np


def update_next(event):
    viewer = next(viewers)
    viewer.data = np.random.normal(size=lst.n_pixel)


lst = LST(position_x=0, position_y=0, telescope_id=0)

root = tk.Tk()
top = tk.Frame(root)
bottom = tk.Frame(root)

viewer1 = TelescopeEventView(top, lst)
viewer2 = TelescopeEventView(top, lst)
viewer3 = TelescopeEventView(top, lst)
viewer4 = TelescopeEventView(bottom, lst)
viewer5 = TelescopeEventView(bottom, lst)
viewer6 = TelescopeEventView(bottom, lst)

viewers = cycle([viewer1, viewer2, viewer3, viewer4, viewer5, viewer6])

viewer1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer4.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer5.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer6.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

root.bind('<Key>', update_next)

top.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
bottom.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
root.mainloop()
