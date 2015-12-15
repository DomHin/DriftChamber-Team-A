from unittest.case import TestCase
from nose_parameterized import parameterized
import inspect
from driftchamber.utils import Introspection

class IntrospectionTest(TestCase):
    
    def setUp(self):
        self._introspect = Introspection()
    
    @parameterized.expand([
        ('collections.abc.Sequence'),
        ('collections.abc.Coroutine'),
        ('collections.abc.Generator')
    ])
    def test_load_class(self, class_fqn):
        cls = self._introspect.load_class(class_fqn)
        self.assertTrue(inspect.isclass(cls))