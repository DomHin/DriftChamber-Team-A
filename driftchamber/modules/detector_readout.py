# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.module import Module
from driftchamber.data.event_container import EventContainer
from driftchamber.data.hit_object import HitObject


class DetectorReadOut(Module):

    def begin(self, datastore):
        datastore.put('HitObjects', EventContainer(), ObjectLifetime.Application)

    def event(self, datastore):
        detector = datastore.get("Detector")
        hitobjects = datastore.get("HitObjects")
        for _, sl in enumerate(detector.detector):
            for layer in sl.layers:
                for cell in layer.cells:
                    if cell.is_triggered():
                        hit = HitObject(cell.pos, cell.energy(), cell)
                        hitobjects.add_object(datastore.get("current_event_index"), hit)
        # reset detector for next event.
        detector.reset()
