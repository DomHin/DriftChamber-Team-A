from unittest.case import TestCase
from os.path import realpath, dirname, join
from driftchamber.run_configuration import YamlConfiguration

class YamlConfigurationTest(TestCase):
    
    def setUp(self):
        current_dir = dirname(realpath(__file__))
        self._config_path = join(current_dir, 'resources', 'dummy.yml')
    
    def test_parse(self):
        config = YamlConfiguration(path=self._config_path, root_node='dummy')
        
        self.assertEqual(config.get_value('a'), 1)
        self.assertEqual(config.get_value('b'), 4)
        self.assertIsInstance(config.get_value('c'), list)
        self.assertListEqual(config.get_value('c'), [1, 2, 3, 4])