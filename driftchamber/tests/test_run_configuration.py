from unittest.case import TestCase
from nose_parameterized import parameterized
from os.path import realpath, dirname, join
from driftchamber.utils import Introspection
from driftchamber.run_configuration import YamlConfiguration, Loader
from driftchamber.modules.hello_world import HelloWorld
from driftchamber.modules.bye_bye_world import ByeByeWorld

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
        
class LoaderTest(TestCase):
    
    def setUp(self):
        introspect = Introspection()
        self._loader = Loader(introspect)
        
    @parameterized.expand([
        ('hello_world.HelloWorld', HelloWorld),
        ('bye_bye_world.ByeByeWorld', ByeByeWorld)
    ])
    def test_load_module(self, module, cls):
        obj = self._loader.load_module(module)
        self.assertIsInstance(obj, cls)