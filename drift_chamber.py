#! /usr/bin/env python3.4

import logging

from core.run_engine import RunEngine
from modules.ByeByeWorldModule import ByeByeWorld
from modules.HelloWorldModule import HelloWorld



def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Drift Chamber project started")

    helloWorldModule = HelloWorld()
    byebyeWorldModule = ByeByeWorld()

    runEngine = RunEngine()
    runEngine.add_module(helloWorldModule)
    runEngine.add_module(byebyeWorldModule)
    runEngine.set_events(100)

    runEngine.run()

    logging.info("All processing done")


if __name__ == "__main__":
    main()
