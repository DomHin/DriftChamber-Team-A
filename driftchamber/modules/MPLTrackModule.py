# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'

import logging

from driftchamber.core.datastore import NotFoundInDataStore
from driftchamber.core.module import Module


class MPLHit(Module):

    def event(self, datastore):
        try:
            subplot = datastore.get("Subplot")
            tracks = datastore.get("Tracks").get_obects(datastore.get("CurrentEvent"))
            detector = datastore.get("Detector")
        except NotFoundInDataStore:
            logging.error("MPLHit: Missing required objects")
            return
        else:
            for track in tracks:
                x, y = track.eval(detector.width, detector.height)
                subplot.plot(x, y, marker='none', color="blue")