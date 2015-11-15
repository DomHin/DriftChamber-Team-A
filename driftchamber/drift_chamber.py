#! /usr/bin/env python3.4

import logging
from configparser import ConfigParser
from argparse import ArgumentParser
import os

from driftchamber.core.run_engine import RunEngine



def main():
    parser = ArgumentParser('Driftchamber Project of Team A')
    parser.add_argument('--config', type=str, default=None,
                        help='The configuration file to load. This overrides --modules and --eventCount.')
    parser.add_argument('--module', type=str, default=None, action='append',
                        help='Specify a module to load. Can be used multiple times to load multiple modules.')
    parser.add_argument('--eventCount', type=int, default=None, help='Specify the amount of events to run.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.info('Drift Chamber project started')

    if args.config:
        if not os.path.isfile(args.config):
            logging.error("Specified config file does not exist")
            return
        config = ConfigParser()
        config.read(args.config)
        # Check if section Modules and option load_modules exists in config file and read the values
        if config.has_option('Modules', 'load_modules'):
            modules = config['Modules']['load_modules'].strip().split('\n')
        else:
            logging.error('No Modules specified')
            return

        # Check if section General and option event_count exists in config file and read values
        if config.has_option('General', 'event_count'):
            event_count = config.getint('General', 'event_count')
        else:
            logging.error('Event Count was not specified')
            return
    elif args.module and args.eventCount:
        modules = args.module
        event_count = args.eventCount
    else:
        if not args.module:
            logging.error('No modules to load.')
        if not args.eventCount:
            logging.error('Number of events (eventCount) has to be specified.')
        return


    # Import modules specified in config file. Create objects of Classes in the module (note:
    # the module Class has to have the same name as the file without Module at the end. e.g.
    # filename: EventModule, classname: Event)
    # Append created objects to module_list
    module_list = []
    for mod in modules:
        try:
            tmp = __import__('modules.'+mod, globals(), locals(), [mod[:-6]])
        except ImportError:
            logging.error('Specified Module does not exist or could not be loaded.')
            return
        try:
            module_list.append(getattr(tmp, mod[:-6])())
        except AttributeError as e:
            logging.error('\''+mod[:-6]+'\' class was not found in module \''+mod+'\'')

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
