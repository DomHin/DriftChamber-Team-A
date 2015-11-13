__author__ = 'Thomas Hauth, Martin Heck'

import os
import functools
from enum import Enum


class NotFoundInDataStore(Exception):
    """
    Exception which gets raised if an object with the
    requested lifetime does not exist in the data store
    """
    pass


class AlreadyInDataStore(Exception):
    """
    Exception which gets raised if an object with the
    same name is already registered in the the data store
    """
    pass


class ObjectLifetime(Enum):
    """
    Enum to represent the lifeime of an data store object

    Objects with Event lifetime will be cleared after one
    event has been processed and before the next one is started

    Object with Application lifetime will persist in the datastore,
    as long as the application is running
    """
    Event = 1
    Application = 2


class DataStore(object):
    """
    Data store for modules to retrieve input for their computation and
    store their resulting products. All entries are indexed by a name.
    """

    def __init__(self):
        # empty-initialize the data-store variable
        self.store = {}

    def put(self, name, obj, lifetime=ObjectLifetime.Event):
        """
        Put a object in the datastore. An object with the same name must not exist,
        otherwise a AlreadyInDataStore exception is thrown
        :param name: identifying name
        :param obj: object to store
        :param lifetime: lifetime of the object
        :return: None
        """

        # check if object with the same name is already stored?
        if name in self.store.keys():
            raise AlreadyInDataStore()
        # no, store it!
        self.store[name] = (lifetime, obj)

    def get(self, name):
        """
        retrieves an object by its name. Can raise a NotFoundInDataStore exception, if
        no object with this name is registered
        :param name: object name
        :return: reference to the object
        """

        if not name in self.store.keys():
            raise NotFoundInDataStore()

        return self.store[name][1]

    def clear(self, lifetime):
        """
        Remove all objects from the datastore which have the lifetime specifies in the
        parameter
        :param lifetime: all objects with this lifetime will be removed from the store
        :return: None
        """

        # find all entries with the specified lifetime
        to_remove = [k for (k, v) in self.store.items() if v[0] == lifetime]
        # remove all these entries from the list
        for t in to_remove:
            del self.store[t]

    def __str__(self):
        """
        Convinience function to convert the data store content into a string
        :return: string representation of the data store content
        """
        return functools.reduce(
            lambda acc, v: acc + str(v[0]) + " : " + str(v[1][1]) + " - lifetime " + str(v[1][0]) + os.linesep,
            self.store.items(), "")

