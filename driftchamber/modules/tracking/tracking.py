# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""

import logging

import numpy as np

from driftchamber.core.datastore import NotFoundInDataStore
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.module import Module
from driftchamber.data.eventcontainer import EventContainer
from driftchamber.modules.TrackingModule.Track import Track


class Tracking(Module):

    def begin(self, datastore):
        configuration = datastore.get(self)
        self.precision = configuration['Tracking_precision']  # n decimals precision. This increases required memory by a lot!

        self.max_distance = 0
        self.rows = 0
        self.columns = 0
        self.radians = []  # numpy calculates using radians but matrix is easier to understand with degrees
        self.parametrisation = "[0] = cos([1]/degree)*x + sin([1]/degree)*y"

        detector = datastore.get("Detector")
        # TODO: consider center-coordinates to reduce size and therefore required memory:
            # Drawback: final parameters are center-coordinates and
            # need to be transformed to our matplotlib coordinates again.
        # calculate size of required array
        self.max_distance = np.round(((detector.height - 1)**2 + (detector.width - 1)**2)**0.5)
        self.columns = (2*self.max_distance + 1)*10**self.precision
        # 0 and 180 are the same -> -1
        self.rows = 10**self.precision * 180 - 1  # 180 degrees times 10**precision
        self.radians = np.radians(np.linspace(0, 180, num=self.rows, endpoint=False))

        datastore.put("Tracks", EventContainer(), ObjectLifetime.Application)

    def event(self, datastore):
        try:
            hitlist = datastore.get('HitObjects').get_objects(datastore.get('current_event_index'))
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
        tracks = datastore.get("Tracks")
        tracks.add_object(datastore.get("current_event_index"), Track(self.parametrisation, (distance, angle), "track"))
        logging.info("track parameters:\t" + str(angle) + "\t" + str(distance))

    def accumulate(self, poslist, matrix):
        for pos in poslist:
            # this returns indices from -d_min to d_max
            distances = pos[0] * np.cos(self.radians) + pos[1] * np.sin(self.radians)
            for i, d in enumerate(distances):
                column = int((d + self.max_distance) * 10**self.precision)
                row = i
                matrix[row, column] += 1



