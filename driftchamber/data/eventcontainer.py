# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'


class EventContainer:
    def __init__(self):
        self._objects = {}

    def add_object(self, event_nr, object):
        if event_nr in self._objects:
            self._objects[event_nr].append(object)
        else:
            self._objects[event_nr] = [object]

    def get_objects(self, event_nr):
        try:
            ret = self._objects[event_nr]
        except KeyError:
            return None
        else:
            return ret