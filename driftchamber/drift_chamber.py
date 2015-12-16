import logging
from argparse import ArgumentParser
from driftchamber.core.run_engine import RunEngine
from driftchamber.run_configuration import RunConfiguration,\
    RunEngineConfigurator, Loader
from driftchamber.utils import Introspection

class DriftChamber(object):
        
    def __init__(self):
        loader = Loader(Introspection())
        self._configurator = RunEngineConfigurator(loader)
        
        self._engine = None
        
    def load_run_config(self, run_config_path):
        self._engine = RunEngine()
        run_config = RunConfiguration(run_config_path)
        
        self._configurator.apply(run_config, self._engine)
    
    def run_sim(self):
        self._engine.execute()

def main(args = None):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Drift Chamber Program started')

    parser = ArgumentParser(description='DriftChamber [Team A]')
    parser.add_argument('runconfiguration', type = str,  required = True,
                        help = 'Path to a run configuration file.')
    args = parser.parse_args(args)

    chamber = DriftChamber()
    chamber.load_run_config(args.runconfiguration)
    chamber.run_sim()

    logging.info('All processing done')

if __name__ == '__main__':
    main()