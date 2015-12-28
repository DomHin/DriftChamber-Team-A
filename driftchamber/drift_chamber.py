import logging
from argparse import ArgumentParser
from driftchamber.core.run_engine import RunEngine
from driftchamber.run_configuration import (
    RunConfiguration, RunEngineConfigurator, ResourceLoader)

def run_simulation(run_config_path):
    loader = ResourceLoader()
    configurator = RunEngineConfigurator(loader)
    run_config = RunConfiguration(run_config_path)
    
    engine = RunEngine()
    configurator.apply(run_config, engine)
    engine.execute()

def main(args = None):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Drift Chamber Simulator started')
    
    parser = ArgumentParser(description='DriftChamber [Team A]')
    parser.add_argument('runconfiguration', type=str, required=True,
                        help='Path to a run configuration file.')
    args = parser.parse_args(args)
    
    run_simulation(args.runconfiguration)
    logging.info('Drift Chamber Simulator finished')

if __name__ == '__main__':
    main()
    