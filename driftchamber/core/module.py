__author__ = 'Thomas Hauth, Martin Heck'


class Module(object):
    """
    Base class for processing modules
    """
    index = 0

    def __init__(self, config=None):
        """
        initializer method without function
        :return: None
        """
        if config == [] or config is None:
            self.config = None
        elif len(config) == 1:
            try:
                self.index = int(config[0])
            except ValueError:
                raise IndexError('Index for module is not an integer. (Exception type is joke :) )')
            self.config = None
        else:
            self.config = config[1:]

    def begin(self, datastore):
        """
        Called by the processing framework before event processing
        starts. Can be used to initialize variables and load required
        data.
        Overwrite this, if your module implementation has such a requirement
        This function is only called once in the application lifetime.

        :param datastore: reference to the DataStore object
        :return: None
        """
        pass

    def event(self, datastore):
        """
        Called by the processing framework for every event during event processing.
        Overwrite this, if your module implementation needs to perform some work on a
        per-event basis. This function is called many times in the application lifetime.

        :param datastore: reference to the DataStore object
        :return: None
        """
        pass

    def end(self, datastore):
        """
        Called by the processing framework after the last event has been processed.
        Overwrite this, if your module implementation needs to perform some work after
        all events have been processed. This function is only called once in the application lifetime.

        :param datastore: reference to the DataStore object
        :return: None
        """
        pass

    def __lt__(self, other):
        if self.index < other.index:
            return True
        return False

    def __gt__(self, other):
        if self.index > other.index:
            return True
        return False

    def __eq__(self, other):
        if self.index == other.index:
            return True
        return False

