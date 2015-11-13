#! /usr/bin/env python3.4

import logging
from configparser import ConfigParser

from core.run_engine import RunEngine



def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Drift Chamber project started')

    config = ConfigParser()
    config.read('config.cfg')
    # Check if section Modules and option load_modules exists in config file and read the values
    if config.has_option('Modules', 'load_modules'):
        modules = config['Modules']['load_modules'].strip().split('\n')
    else:
        print('No Modules specified')
        return

    # Check if section General and option event_count exists in config file and read values
    if config.has_option('General', 'event_count'):
        event_count = config.getint('General', 'event_count')
    else:
        print('Event Count was not specified')
        return

    # Import modules specified in config file. Create objects of Classes in the module (note:
    # the module Class has to have the same name as the file without Module at the end. e.g.
    # filename: EventModule, classname: Event)
    # Append created objects to module_list
    module_list = []
    for mod in modules:
        tmp = __import__('modules.'+mod, globals(), locals(), [mod[:-6]])
        module_list.append(getattr(tmp, mod[:-6])())

    runEngine = RunEngine()

    # Register every module in module_list in runEngine
    for mod in module_list:
        runEngine.add_module(mod)
    runEngine.set_events(event_count)

    # Run simulation
    runEngine.run()

    logging.info('All processing done')


if __name__ == '__main__':
    main()
