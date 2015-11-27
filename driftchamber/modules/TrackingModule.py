# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""

import numpy as np
from driftchamber.core.module import Module
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.datastore import NotFoundInDataStore
import logging


class Tracking(Module):

    def __init__(self):
        super(Tracking, self).__init__()
        # TODO: config argument
        self.precision = 1  # n decimals precision. This increases required memory by a lot!

        self.max_distance = 0
        self.rows = 0
        self.columns = 0
        self.radians = []  # numpy calculates with radians but matrix is easier to understand with degrees
        self.geometry_width = 0
        self.geometry_heigt = 0

    def begin(self, datastore):
        try:
            detector = datastore.get("Detector")
        except NotFoundInDataStore:
            return
        # TODO: consider center-coordinates to reduce size:
            # Drawback: final parameters are center-coordinates and
            # need to be transformed to our matplotlib coordinates again.
        # calculate size of required array
        self.max_distance = np.round(((detector.height - 1)**2 + (detector.width - 1)**2)**0.5)
        self.columns = (2*self.max_distance + 1)*10**self.precision
        # 0 and 180 are the same -> -1
        self.rows = 10**self.precision * 180 - 1  # 180 degrees times 10**precision
        self.radians = np.radians(np.linspace(0, 180, num=self.rows, endpoint=False))

        self.geometry_heigt = detector.height
        self.geometry_width = detector.width

        # TODO: create Trackcontainer in datastore
        #self.datastore.put("Tracks", TrackObjects)

    def event(self, datastore):
        if self.geometry_heigt is None or self.geometry_width is None:
            return
        if self.rows is None or self.columns is None:
            return
        try:
            hitlist = datastore.get('HitObjects').get_all_hits(datastore.get('CurrentEvent'))
        except NotFoundInDataStore:
            return
        # create poslist instead of hitlist to reduce depth and ignore other information than position.
        poslist = []
        for hit in hitlist:
            poslist.append((hit.pos[0], hit.pos[1]))
        # TODO: If algorithm too slow or hungry change this module implementation to fast hugh algorithm.
        # This matrix gets huge with precision.
        vote_mat = np.zeros((self.rows, self.columns), dtype='int')
        self.accumulate(poslist, vote_mat)

        # TODO: search for more than one track. We will need to find several peaks and discriminate them from noise
        i, j = np.unravel_index(vote_mat.argmax(), vote_mat.shape)
        angle = i / (10**self.precision)
        distance = j / 10**self.precision - self.max_distance
        # TODO: pass to trackcontainer
        try:
            datastore.put("track", (angle, distance), ObjectLifetime.Application)
        except:
            pass
        logging.info("track parameters:\t" + str(angle) + "\t" + str(distance))

    def accumulate(self, poslist, matrix):
        for pos in poslist:
            # this returns indices from -d_min to d_max
            distances = pos[0] * np.cos(self.radians) + pos[1] * np.sin(self.radians)
            for i, d in enumerate(distances):
                column = int((d + self.max_distance) * 10**self.precision)
                row = i
                matrix[row, column] += 1



