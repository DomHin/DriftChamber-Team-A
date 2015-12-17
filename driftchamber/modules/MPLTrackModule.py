# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import logging

import matplotlib.cm as cm

from driftchamber.core.datastore import NotFoundInDataStore
from driftchamber.core.module import Module

class MPLTrack(Module):

    def begin(self, datastore):
        # These could be transformed to parameters
        self.colormap = cm.get_cmap("winter")
        self.linewidth = 2

    def event(self, datastore):
        try:
            subplot = datastore.get("Subplot")
            tracks = datastore.get("Tracks").get_objects(datastore.get("current_event_index"))
            detector = datastore.get("Detector")
        except NotFoundInDataStore:
            logging.error("MPLTrack: Missing required objects")
            return
        else:
            if not tracks:
                return
            for track in tracks:
                x, y = track.eval(detector.width, detector.height)
                subplot.plot(x, y, marker='None', color=self.colormap(track.probability), linewidth=self.linewidth)
