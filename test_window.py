from telescope import LST
from windows import TelescopeEventView
import tkinter as tk
import numpy as np

lst = LST(position_x=0, position_y=0, telescope_id=0)

root = tk.Tk()
viewer1 = TelescopeEventView(root, lst, np.random.normal(size=lst.n_pixel))
viewer2 = TelescopeEventView(root, lst, np.random.normal(size=lst.n_pixel))
viewer1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
viewer2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
root.mainloop()
