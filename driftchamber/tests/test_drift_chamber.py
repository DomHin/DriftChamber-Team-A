from unittest.case import TestCase
from testfixtures import log_capture
from driftchamber.drift_chamber import run_simulation
from driftchamber.tests.resources import resource_path

class DriftChamberTest(TestCase):
    
    @log_capture()
    def test_basic_simulation(self, log):
        config_path = resource_path('run_configuration_basic.yml')
        run_simulation(config_path)
        
        log.check(
            ('root', 'INFO', 'Module HelloWorld processing event #1'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #1'),
            ('root', 'INFO', 'Module HelloWorld processing event #2'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #2'),
            ('root', 'INFO', 'Module HelloWorld processing event #3'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #3'),
            ('root', 'INFO', 'Module HelloWorld processing event #4'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #4'),
            ('root', 'INFO', 'Module HelloWorld processing event #5'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #5'))