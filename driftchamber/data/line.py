# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
import numpy as np


class LineObject(object):
    def __init__(self, parametrisation, parameters, identifier):
        """
        Baseobject that can be represented by a continious line.
        :param string identifier: type of object
        :param tuple parameters: tuple of parameters that define this object in regard to its parametrisation
        :param string parametrisation: String representation of used parametrisation.
        :return:
        """
        self.identifier = identifier
        self.parametrisation = parametrisation
        self.parameters = parameters

    def eval(self, width, height):
        """
        Calculates x- and y-coordinates from given figure size.
        :param width: width of figure (width of detector)
        :param height: height of figure (heigt  of detector)
        :return numpy arrays: x, y
        """
        print("not implemented!")
        return np.array([]), np.array([])