from unittest import TestCase
from driftchamber.args import ProgramArguments

class ProgramArgumentsTest(TestCase):
    
    def test_config_path(self):
        rawargs = { '--configpath': 'testfile' }
        args = ProgramArguments(rawargs)
        
        self.assertEqual(self, args.config_path(), rawargs['configpath'])