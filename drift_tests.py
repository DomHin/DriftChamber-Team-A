#! /usr/bin/env python3.4

import unittest
import sys

def main():
    all_test = unittest.defaultTestLoader.discover("")
    if unittest.TextTestRunner(verbosity=2).run(all_test).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
