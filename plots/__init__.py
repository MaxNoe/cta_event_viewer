import matplotlib
matplotlib.use('tkagg')
import numpy as np
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection


class CameraPlot(object):
    '''A Class for a camera pixel'''

    def __init__(
        self,
        telescope,
        ax,
        data=None,
        cmap='gray',
        vmin=None,
        vmax=None,
    ):
        '''
        :telescope: the telescope class for the pixel
        :data: array-like with one value for each pixel
        :cmap: a matpixellib colormap string or instance
        :vmin: minimum value of the colormap
        :vmax: maximum value of the colormap

        '''
        self.telescope = telescope
        if data is None:
            data = np.zeros(telescope.n_pixel)

        patches = []
        if telescope.pixel_shape == 'hexagon':
            for xy in zip(telescope.pixel_x, telescope.pixel_y):
                patches.append(
                    RegularPolygon(
                        xy=xy,
                        numVertices=6,
                        radius=telescope.pixel_size,
                        orientation=telescope.pixel_orientation,
                    )
                )
        self.pixel = PatchCollection(patches)
        self.pixel.set_linewidth(0)
        self.pixel.set_cmap(cmap)
        self.pixel.set_array(data)
        self.pixel.set_clim(vmin, vmax)
        self.vmin = vmin
        self.vmax = vmax
        self.ax = ax
        self.ax.axis('off')
        self.ax.add_collection(self.pixel)
        self.ax.set_xlim(
            self.telescope.pixel_x.min() - self.telescope.pixel_size,
            self.telescope.pixel_x.max() + self.telescope.pixel_size,
        )
        self.ax.set_ylim(
            self.telescope.pixel_y.min() - self.telescope.pixel_size,
            self.telescope.pixel_y.max() + self.telescope.pixel_size,
        )

    @property
    def data(self):
        return self.pixel.get_array()

    @data.setter
    def data(self, data):
        self.pixel.set_array(data)
        if not self.vmin or not self.vmax:
            self.pixel.autoscale()
        self.pixel.changed()
