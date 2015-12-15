from unittest.case import TestCase
from driftchamber.run_configuration import YamlConfiguration

class YamlConfigurationTest(TestCase):
    
    def test_parse(self):
        config = YamlConfiguration()