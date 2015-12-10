from unittest import TestCase
from driftchamber.core.factory import ModuleFactory
from driftchamber.core.module import Module

class ModuleFactoryTest(TestCase):

    def test_create_instance(self):
        module = ModuleFactory.create_instance('hello_world')
        self.assertIsInstance(module, Module)