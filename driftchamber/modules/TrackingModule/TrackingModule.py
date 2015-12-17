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
        self.threshold = configuration['Tracking_threshold']
        self.minDistance = configuration['Tracking_minDistance']

        self.max_distance = 0
        self.rows = 0
        self.columns = 0
        self.radians = []  # numpy calculates using radians but matrix is easier to understand with degrees
        self.parametrisation = "[0] = cos([1]/degree)*x + sin([1]/degree)*y"

        detector = datastore.get("Detector")
        # calculate size of required array
        self.max_distance = np.round(((detector.height - 1)**2 + (detector.width - 1)**2)**0.5)
        self.columns = (2*self.max_distance + 1)*10**self.precision
        # 0 and 180 are the same -> -1
        self.rows = 10**self.precision * 180 - 1  # 180 degrees times 10**precision
        self.radians = np.radians(np.linspace(0, 180, num=self.rows, endpoint=False))

        datastore.put("Tracks", EventContainer(), ObjectLifetime.Application)

    def event(self, datastore):
        # Gather objects
        tracks = datastore.get("Tracks")
        try:
            hitlist = datastore.get('HitObjects').get_objects(datastore.get('current_event_index'))
        except NotFoundInDataStore:
            return
        # create poslist instead of hitlist to reduce depth and ignore other information than position.
        poslist = []
        for hit in hitlist:
            poslist.append((hit.pos[0], hit.pos[1]))

        # Reconstruct Tracks
        # This matrix gets huge with precision.
        vote_mat = np.zeros((self.rows, self.columns), dtype='int')
        self.accumulate(poslist, vote_mat)

        track_results = self.select_tracks(vote_mat)
        for track in track_results:
            tracks.add_object(datastore.get("current_event_index"), track)

    def select_tracks(self, matrix):
        tracks = []
        indice_list = []

        i, j = np.unravel_index(matrix.argmax(), matrix.shape)
        indice_list.append((i, j))
        for z in range(matrix.max(), self.threshold, -1):
            indices = np.where(matrix == z)

            for i in range(len(indices[0])):
                append = True
                for tupl in indice_list:
                    if ((tupl[0]-indices[0][i])**2 + (tupl[1]-indices[1][i])**2)**0.5 <= self.minDistance:
                        append = False
                if append:
                    indice_list.append((indices[0][i], indices[1][i]))

        for tupl in indice_list:
            tracks.append(self.generate_track(tupl, matrix[tupl]))
        return tracks

    def generate_track(self, indices, maximum):
        angle = indices[0] / (10**self.precision)
        distance = indices[1] / 10**self.precision - self.max_distance

        # calculate times threshold
        value = maximum - self.threshold
        if value < 0:
            value = 0
        value /= self.threshold

        probability = value
        hough_hits = maximum

        # generate logging message for this track
        tracking_message = "track parameters:\t" + str(distance) + "\t" + str(angle)
        tracking_message += "\tHoughHits:\t" + str(hough_hits) + "\tTimes Threshold:\t" + str(probability)
        logging.info(tracking_message)

        return Track(self.parametrisation, (distance, angle), "track", probability)

    def accumulate(self, poslist, matrix):
        for pos in poslist:
            # this returns indices from -d_min to d_max
            distances = pos[0] * np.cos(self.radians) + pos[1] * np.sin(self.radians)
            for i, d in enumerate(distances):
                column = int((d + self.max_distance) * 10**self.precision)
                row = i
                matrix[row, column] += 1



