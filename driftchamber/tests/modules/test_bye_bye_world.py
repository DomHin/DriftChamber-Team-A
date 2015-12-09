import unittest

from testfixtures import LogCapture
from driftchamber.core.datastore import DataStore
from driftchamber.modules.ByeByeWorldModule import ByeByeWorld

class ByeByeWorldModuleTest(unittest.TestCase):
    """
    Test class for the HelloWorldModule
    """

    def test_run(self):
        datastore = DataStore()
        module = ByeByeWorld()
        with LogCapture() as logCapture:
            module.begin(datastore)
            module.event(datastore)
            module.event(datastore)
            module.end(datastore)
            logCapture.check(
                    ('root', 'INFO', "Begin of module 'ByeByeWorld'"),
                    ('root', 'INFO', "Number of previous events in module 'ByeByeWorld': 1"),
                    ('root', 'INFO', "Number of previous events in module 'ByeByeWorld': 2"),
                    ('root', 'INFO', "End of module 'ByeByeWorld'")
            )