from unittest.case import TestCase
from nose_parameterized import parameterized
import inspect
from driftchamber.core.datastore import ObjectLifetime
from driftchamber.run_configuration import (
    YamlConfiguration, RunConfiguration, ResourceLoader, RunEngineConfigurator)
from driftchamber.modules.hello_world import HelloWorld
from driftchamber.modules.bye_bye_world import ByeByeWorld
from driftchamber.modules.geometry import DetectorGeometry
from driftchamber.core.run_engine import RunEngine
from driftchamber.tests.resources import resource_path

class YamlConfigurationTest(TestCase):

    def test_dummy_file(self):
        dummy_path = resource_path('dummy.yml')
        config = YamlConfiguration(path = dummy_path, root_node = 'dummy')
        
        self.assertEqual(config.get_value('a'), 1)
        self.assertEqual(config.get_value('b'), 4)
        self.assertEqual(config.get_value('nonexisting'), None)
        self.assertEqual(config.get_value('nonexisting1', 0), 0)
        self.assertIsInstance(config.get_value('c'), list)
        self.assertListEqual(config.get_value('c'), [1, 2, 3, 4])

class RunConfigurationTest(TestCase):

    def test_basic_configuration(self):
        config_path = resource_path('run_configuration_basic.yml')
        
        config = RunConfiguration(config_path)
        expected_modules = ['hello_world.HelloWorld', 
                            'bye_bye_world.ByeByeWorld']
        
        self.assertEqual(config.get_value('events'), 5)
        self.assertListEqual(config.get_value('modules'), expected_modules)
        
class ResourceLoaderTest(TestCase):

    @parameterized.expand([
        ('hello_world.HelloWorld', HelloWorld),
        ('bye_bye_world.ByeByeWorld', ByeByeWorld)
    ])
    def test_load_module(self, module, cls):
        loader = ResourceLoader()
        obj = loader.load_module(module)
        self.assertIsInstance(obj, cls)
        
    @parameterized.expand([
        ('collections.abc.Sequence'),
        ('collections.abc.Coroutine'),
        ('collections.abc.Generator')
    ])
    def test_load_class(self, class_fqn):
        loader = ResourceLoader()
        cls = loader.load_class(class_fqn)
        self.assertTrue(inspect.isclass(cls))
        
class RunEngineConfiguratorTest(TestCase):

    def test_basic_configuration(self):
        config_path = resource_path('run_configuration_basic.yml')

        engine = RunEngine()
        configurator = RunEngineConfigurator(ResourceLoader())
        configurator.apply(RunConfiguration(config_path), engine)

        self.assertEqual(engine.events, 5)
        self.assertIsInstance(engine._modules[0], HelloWorld)
        self.assertIsInstance(engine._modules[1], ByeByeWorld)
        
    def test_configuration_with_parameters(self):
        config_path = resource_path('run_configuration_params.yml')

        engine = RunEngine()
        configurator = RunEngineConfigurator(ResourceLoader())
        configurator.apply(RunConfiguration(config_path), engine)

        self.assertEqual(engine.events, 0)
        self.assertIsInstance(engine._modules[0], HelloWorld)
        self.assertIsInstance(engine._modules[1], DetectorGeometry)
        self.assertIsInstance(engine._modules[2], ByeByeWorld)
        self.assertEqual(engine._modules[1]._superlayers, 4)
        self.assertListEqual(engine._modules[1]._layers, [4, 2, 5, 1])
        self.assertEqual(engine._modules[1]._cells, 5)
        
    def test_configuration_with_datastore_objects(self):
        config_path = resource_path('run_configuration_datastore_objects.yml')

        engine = RunEngine()
        configurator = RunEngineConfigurator(ResourceLoader())
        configurator.apply(RunConfiguration(config_path), engine)
        
        datastore = engine._datastore
        electron = datastore.get('electron')
        
        self.assertEqual(datastore.store['electron'][0], ObjectLifetime.Event)
        self.assertEqual(electron.name, 'electron')
        self.assertEqual(electron.mass, 0.000501)
        self.assertEqual(electron.momentum[0], 0.04)
        self.assertEqual(electron.momentum[1], 0.06)
        