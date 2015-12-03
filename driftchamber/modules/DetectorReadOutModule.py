# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.module import Module
from driftchamber.data.eventcontainer import EventContainer
from driftchamber.data.hitObject import HitObject


class DetectorReadOut(Module):

    def begin(self, datastore):
        datastore.put('HitObjects', EventContainer(), ObjectLifetime.Application)

    def event(self, datastore):
        detector = datastore.get("Detector")
        hitobjects = datastore.get("HitObjects")
        for idx, sl in enumerate(detector.detector):
            for layer in sl.layers:
                for cell in layer.cells:
                    if cell.is_triggered():
                        hit = HitObject(cell.pos, cell.energy(), cell)
                        hitobjects.add_object(datastore.get("CurrentEvent"), hit)
        # reset detector for next event.
        detector.reset()
