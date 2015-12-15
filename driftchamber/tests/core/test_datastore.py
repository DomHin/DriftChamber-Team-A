__author__ = 'Thomas Hauth, Martin Heck'

import unittest

from driftchamber.core.datastore import DataStore, NotFoundInDataStore, \
    AlreadyInDataStore, ObjectLifetime

class DataStoreTest(unittest.TestCase):
    """
    Test class for the DataStore class
    """

    def test_put_get_scalar(self):
        ds = DataStore()
        ds.put('int1', 10)
        ds.put('int2', 20)

        self.assertEqual(ds.get('int1'), 10)
        self.assertEqual(ds.get('int2'), 20)

    def test_get_invalid(self):
        ds = DataStore()

        with self.assertRaises(NotFoundInDataStore):
            ds.get("not_set")

    def test_ref_assumption_val_type(self):
        ds = DataStore()
        ds.put('item', 20)
        ds.get('item')

        self.assertEqual(ds.get('item'), 20)

    def test_ref_assumption_ref_type(self):
        ds = DataStore()

        class WrappedInt(object):
            def __int__(self):
                self.i = 20

        ds.put('item', WrappedInt())
        item = ds.get("item")
        item.i = 40

        self.assertEqual(ds.get('item').i, 40)

    def test_put_twice(self):
        ds = DataStore()
        ds.put('item', 20)
        with self.assertRaises(AlreadyInDataStore):
            ds.put('item', 10)

    def test_lifetime(self):
        ds = DataStore()
        # implicit event lifetime
        ds.put('item1', 20)
        # explicit event lifetime
        ds.put('item2', 30, ObjectLifetime.Event)
        # explicit application lifetime
        ds.put('item3', 40, ObjectLifetime.Application)

        ds.clear(ObjectLifetime.Event)

        with self.assertRaises(NotFoundInDataStore):
            ds.get('item1')
        with self.assertRaises(NotFoundInDataStore):
            ds.get('item2')

        self.assertIsNotNone(ds.get('item3'))

        ds.clear(ObjectLifetime.Application)

        with self.assertRaises(NotFoundInDataStore):
            ds.get('item3')