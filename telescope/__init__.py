import pandas as pd

lst_mapping = pd.read_csv('telescope/lst.csv')

class Telescope(object):
    """The base Telescope class"""


    def __init__(self, position_x, position_y, telescope_id):
        """
        :position_x: x position of the telescope in meter
        :position_y: y position of the telescope in meter
        :id: id of the telescope
        """
        self.position_x = position_x
        self.position_y = position_y
        self.telescope_id = telescope_id


class LST(Telescope):
    """the CTA large size telescope"""
    pixel_x = lst_mapping.pixel_x.values
    pixel_y = lst_mapping.pixel_y.values
    n_pixel = len(pixel_x)
    pixel_shape = 'hexagon'

    def __init__(self, position_x, position_y, telescope_id):
        super().__init__(position_x, position_y, telescope_id)
