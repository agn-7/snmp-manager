#!/usr/bin/env python

from event_loop.event_loop import EventLoop

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


if __name__ == "__main__":
    print('SNMP Begins')

    try:
        EventLoop().run_forever()

    except KeyboardInterrupt:
        import sys
        sys.exit(0)
