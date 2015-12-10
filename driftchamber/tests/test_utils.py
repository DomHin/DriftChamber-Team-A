from unittest import TestCase
from driftchamber.utils import Introspection

class IntrospectionTest(TestCase):
    
    def test_underscore_to_camelcase(self):
        Introspection.underscore_to_camelcase('a_b_C_e')