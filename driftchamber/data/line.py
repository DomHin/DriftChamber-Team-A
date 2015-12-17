# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
import numpy as np


class LineObject(object):
    def __init__(self, parametrisation, parameters, identifier, probability=1.):
        """
        Base object that can be represented by a continuous line.
        :param string identifier: type of object
        :param tuple parameters: tuple of parameters that define this object in regard to its parameterization
        :param string parameterization: String representation of used parameterization.
        :param float probability: probability if this line was reconstructed correctly.
        :return:
        """
        self.identifier = identifier
        self.parametrisation = parametrisation
        self.probability = probability
        self.parameters = parameters

    def eval(self, width, height):
        """
        Calculates x- and y-coordinates from given figure size.
        :param width: width of figure (width of detector)
        :param height: height of figure (height  of detector)
        :return numpy arrays: x, y
        """
        print("not implemented!")
        return np.array([]), np.array([])