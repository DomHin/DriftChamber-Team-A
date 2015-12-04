
from driftchamber.core.RunEngineFactory import RunEngineFactory
from driftchamber.core.module import Module

class MultiModule(Module):

    def begin(self, datastore):
        configuration = datastore.get(self)
        self._run_engine = RunEngineFactory(configuration['MultiModule_moduleSequence'], datastore).get_run_engine()
        self._run_engine.call_all_begin_methods()
        

    def event(self, datastore):
        self._run_engine.call_next_event_methods()
        

    def end(self, datastore):
        self._run_engine.call_all_end_methods()
