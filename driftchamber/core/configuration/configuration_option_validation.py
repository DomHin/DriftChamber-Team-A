"""
Created on Nov 26, 2015

@author: Fabian Leven
"""

class ConfigurationOptionValidation:
    """
    A class that enables verifying if the value specified for an option is valid.
    """
    def __init__(self,
                 p_validationFunction, 
                 p_failureMessage):
        """
        Constructor.
        :param p_validationFunction  a function that takes a value for an option as parameter 
                              and evaluates to true if the value is valid, e.g.::
                                lambda value: value > 0
        :param p_failureMessage      an error message used in case the validation fails.
        """
        self.validationFunction = p_validationFunction
        self.failureMessage = p_failureMessage