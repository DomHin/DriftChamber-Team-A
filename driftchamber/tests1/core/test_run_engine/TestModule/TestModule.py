# -*- coding: utf-8 -*-

from driftchamber.core.module import Module

class Test(Module):
    def __init__(self):
        self.beginCalled = 0
        self.eventCalled = 0
        self.endCalled = 0
    
    def begin(self, data_store):
        self.beginCalled += 1

    def event(self, data_store):
        self.eventCalled += 1

    def end(self, data_store):
        self.endCalled += 1