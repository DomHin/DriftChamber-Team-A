# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
import logging

import numpy as np

from driftchamber.core.datastore import NotFoundInDataStore
from driftchamber.core.module import Module


class MPLHit(Module):

    def event(self, datastore):
        try:
            subplot = datastore.get("Subplot")
            hits = datastore.get("HitObjects").get_objects(datastore.get("CurrentEvent"))
        except NotFoundInDataStore:
            logging.error("MPLHit: Missing required objects.")
        else:
            x = np.array([hit.pos[0] for hit in hits])
            y = np.array([hit.pos[1] for hit in hits])
            subplot.plot(x, y, marker='s', fillstyle="full", color="red", linestyle="none")
