# -*- coding: utf-8 -*-
"""
@author: elcerdo
"""
__author__ = 'elcerdo'
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

from driftchamber.core.datastore import ObjectLifetime
from driftchamber.core.module import Module


class MPLDisplay(Module):

    def begin(self, datastore):
        self.folder = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".." + os.path.sep + "results" + os.path.sep
        # check if already existing. (Only works secure in single-thread program):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        # try cleaning up files.
        for the_file in os.listdir(self.folder):
            file_path = os.path.join(self.folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except:
                pass

        mpl.rcParams["backend"] = "TkAgg"
        mpl.rcParams["interactive"] = True

        fig = plt.figure()
        self.subplot = fig.add_subplot(111)

        datastore.put("Subplot", self.subplot, ObjectLifetime.Application)

    def event(self, datastore):
        detector = datastore.get("Detector")
        plt.ylim(-0.5, detector.height-0.5)
        plt.xlim(-0.5, detector.width-0.5)
        plt.savefig(self.folder + str(datastore.get("current_event_index")) + ".png", format="png")
        self.subplot.clear()
        return




