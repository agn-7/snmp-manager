#!/usr/bin/env python

try:
    from event_loop import run
except:
    from .event_loop import run

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


if __name__ == "__main__":
    run()
