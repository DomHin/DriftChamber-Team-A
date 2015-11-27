"""
Created on Nov 26, 2015

@author: Fabian Leven
"""


class ConfigurationOption:
    """
    An option that can be configured.
    """

    def __init__(self, 
                 p_key,
                 p_description,
                 p_parseFunction = None, 
                 p_listOfValidation = None,
                 p_isCompulsory = True):
        """
        Constructor.
        
        :param p_key              a unique identifier within the given section of the configuration.
        :param p_description      a description.
        :param p_parseFunction    a function to convert the configuration value ('string') 
                           to the desired format (e.g. 'int').
        :param p_listOfValidation      a list of specifications the configuration value must satisfy, 
                           see examples below.
        :param p_isCompulsory     weather the configuration option must be present ('True') 
                           in the configuration or not ('False').
        """
        self.key = p_key
        self.description = p_description
        self.parseFunction = (lambda x: x) if p_parseFunction is None else p_parseFunction
        self.listOfTests = [] if p_listOfValidation is None else p_listOfValidation
        self.isCompulsory = p_isCompulsory
        # set later to enable a convenient way of entering options into the code
        self.section = ''
        
    def get_full_key(self):
        """
        :return: a unique identifier for this option.
        """
        return self.section + '_' + self.key