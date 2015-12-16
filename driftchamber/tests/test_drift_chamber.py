from unittest.case import TestCase
from testfixtures import log_capture
from os.path import realpath, dirname, join
from driftchamber.drift_chamber import DriftChamber

class DriftChamberTest(TestCase):
    
    @log_capture()
    def test_basic_simulation(self, log):
        current_dir = dirname(realpath(__file__))
        config_path = join(current_dir, 'resources', 
                                 'run_configuration_basic.yml')
        
        chamber = DriftChamber()
        chamber.load_run_config(config_path)
        chamber.run_sim()
        
        log.check(
            ('root', 'INFO', 'Module HelloWorld before event processing'),
            ('root', 'INFO', 'Module ByeByeWorld before event processing'),
            ('root', 'INFO', 'Module HelloWorld processing event #1'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #1'),
            ('root', 'INFO', 'Module HelloWorld processing event #2'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #2'),
            ('root', 'INFO', 'Module HelloWorld processing event #3'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #3'),
            ('root', 'INFO', 'Module HelloWorld processing event #4'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #4'),
            ('root', 'INFO', 'Module HelloWorld processing event #5'),
            ('root', 'INFO', 'Module ByeByeWorld processing event #5'),
            ('root', 'INFO', 'Module HelloWorld after event processing'),
            ('root', 'INFO', 'Module ByeByeWorld after event processing'))