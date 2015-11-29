import unittest

from testfixtures import LogCapture
from driftchamber.core.datastore import DataStore
from driftchamber.modules.HelloWorldModule import HelloWorld

class HelloWorldModuleTest(unittest.TestCase):
    """
    Test class for the HelloWorldModule
    """

    def test_run(self):
        datastore = DataStore()
        module = HelloWorld()
        with LogCapture() as logCapture:
            module.begin(datastore)
            module.event(datastore)
            module.event(datastore)
            module.end(datastore)
            logCapture.check(
                    ('root', 'INFO', "Begin of module 'HelloWorld'"),
                    ('root', 'INFO', "Number of previous events in module 'HelloWorld': 1"),
                    ('root', 'INFO', "Number of previous events in module 'HelloWorld': 2"),
                    ('root', 'INFO', "End of module 'HelloWorld'")
            )