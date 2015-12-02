# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
from driftchamber.core.module import Module


class MPLDetector(Module):

    def begin(self, datastore):
        self._detector = datastore.get("Detector")

    def event(self, datastore):
        subplot = datastore.get('Subplot')
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'black', 'magenta', 'purple', 'lightblue', 'grey']
        for idx, sl in enumerate(self._detector.detector):
            x = []
            y = []
            for layer in sl.layers:
                for cell in layer.cells:
                    x.append(cell.pos[0])
                    y.append(cell.pos[1])

            subplot.plot(x, y, marker='s', fillstyle='none', color=colors[idx % len(colors)], linestyle='none')
