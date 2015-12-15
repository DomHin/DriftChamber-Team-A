import logging
from argparse import ArgumentParser
from driftchamber.core.run_engine import RunEngine
from driftchamber.run_configuration import RunConfiguration

def main(args = None):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Drift Chamber Program started')

    parser = ArgumentParser(description='DriftChamber [Team A]')
    parser.add_argument('--runconfiguration', type = str, 
                        help = 'Path to a run configuration file.')
    args = parser.parse_args(args)
    
    config = RunConfiguration(args.runconfiguration)

    engine = RunEngine()
    engine.nr_events(config.nr_events())
    
    for data_object in config.datastore_objects():
        pass
    
    for module in config.modules():
        pass
    
    engine.execute()

    logging.info('All processing done')

if __name__ == '__main__':
    main()