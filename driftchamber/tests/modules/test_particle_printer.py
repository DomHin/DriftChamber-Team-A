import unittest

from testfixtures import LogCapture
from driftchamber.modules.particle_printer import ParticlePrinter
from driftchamber.core.datastore import DataStore, ObjectLifetime

from driftchamber.core.particles import Particle
from driftchamber.data.particle_container import ParticleContainer


class ParticlePrinterTest(unittest.TestCase):
    """
    Test class for the ParticlePrinter class
    """
    def setUp(self):
        self.datastore = DataStore()
        self.module = ParticlePrinter()
        self.datastore.put('Particles', ParticleContainer(), ObjectLifetime.Application)
        particle = Particle(0.1, 'electron', 5, 0, 0.001, 0.005) #Create Particle with determined specification for read out with the printer
        self.datastore.get('Particles').add_particle(particle, 'electron')


    def test_begin(self):
        with LogCapture() as l:
            self.module.begin(self.datastore)

            l.check(
                    ('root', 'INFO', "Begin of module 'ParticlePrinter'")
            )

    def test_event(self):
        with LogCapture() as l:
            self.module.event(self.datastore)

            l.check(
                    ('root', 'INFO', "Particle: electron"),
                    ('root', 'INFO', "Position\nx=5\ny=0"),
                    ('root', 'INFO', "Momentum\np_x=0.001\np_y=0.005"),

            )

    def test_end(self):
        with LogCapture() as l:
            self.module.end(self.datastore)
            l.check(
                    ('root', 'INFO', "End of module 'ParticlePrinter'")
            )

