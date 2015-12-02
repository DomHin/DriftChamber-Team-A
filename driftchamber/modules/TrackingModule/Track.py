# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import numpy as np

from driftchamber.data.line import LineObject


class Track(LineObject):

    def eval(self, width, height):
        if(self.parameters[1] == 0):
            x = np.array([self.parameters[0], self.parameters[0]])
            y = np.array([0, height])
        else:
            x = np.arange(width)
            y = (self.parameters[0]-np.cos(np.radians(self.parameters[1])))/np.sin(np.radians(self.parameters[1]))
            # Here you could ensure that all values are inside the width and height
        return x, y