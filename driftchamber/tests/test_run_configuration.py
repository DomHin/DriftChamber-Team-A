from unittest.case import TestCase
from nose_parameterized import parameterized
from os.path import realpath, dirname, join
from driftchamber.utils import Introspection
from driftchamber.run_configuration import YamlConfiguration,\
    RunConfiguration, Loader, RunEngineConfigurator
from driftchamber.modules.hello_world import HelloWorld
from driftchamber.modules.bye_bye_world import ByeByeWorld
from driftchamber.core.run_engine import RunEngine

class YamlConfigurationTest(TestCase):
    
    def setUp(self):
        current_dir = dirname(realpath(__file__))
        config_path = join(current_dir, 'resources', 'dummy.yml')
        
        self._config = YamlConfiguration(path = config_path, 
                                         root_node = 'dummy')
    
    def test_parse(self):
        self.assertEqual(self._config.get_value('a'), 1)
        self.assertEqual(self._config.get_value('b'), 4)
        self.assertIsInstance(self._config.get_value('c'), list)
        self.assertListEqual(self._config.get_value('c'), [1, 2, 3, 4])
 
class RunConfigurationTest(TestCase):
    
    def setUp(self):
        current_dir = dirname(realpath(__file__))
        config_path = join(current_dir, 'resources', 
                           'run_configuration_basic.yml')
        self._config = RunConfiguration(config_path)
        
    def test_parse(self):
        self.assertEqual(self._config.get_value('nr_events'), 5)
        self.assertListEqual(self._config.get_value('modules'), 
                             ['hello_world.HelloWorld', 
                              'bye_bye_world.ByeByeWorld'])
        
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
        
class RunEngineConfigurationTest(TestCase):
    
    def setUp(self):
        self._set_up_run_config()
        self._set_up_run_engine_config()
        
    def _set_up_run_config(self):
        current_dir = dirname(realpath(__file__))
        config_path = join(current_dir, 'resources', 
                           'run_configuration_basic.yml')
        self._config = RunConfiguration(config_path)
        
    def _set_up_run_engine_config(self):
        introspect = Introspection()
        loader = Loader(introspect)
        self._configurator = RunEngineConfigurator(loader)
        
    def test_apply(self):
        engine = RunEngine()
        self._configurator.apply(self._config, engine)
        
        self.assertEqual(engine._nr_events, 5)
        self.assertIsInstance(engine._modules[0], HelloWorld)
        self.assertIsInstance(engine._modules[1], ByeByeWorld)