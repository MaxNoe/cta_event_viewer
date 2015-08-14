import tkinter as tk
import matplotlib
matplotlib.use('tkagg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from plots import CameraPlot


class TelescopeEventView(tk.Frame):
    """ A frame showing the camera view of a single telescope """

    def __init__(self, root, telescope, data=None, *args, **kwargs):
        self.telescope = telescope
        super().__init__(root)
        self.figure = Figure(figsize=(5, 5), facecolor='none')
        self.ax = self.figure.add_subplot(1, 1, 1, aspect=1)
        self.camera_plot = CameraPlot(telescope, self.ax, data, *args, **kwargs)
        self.figure.set_tight_layout(True)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    @property
    def data(self):
        return self.camera_plot.data

    @data.setter
    def data(self, value):
        self.camera_plot.data = value
        self.canvas.draw()
