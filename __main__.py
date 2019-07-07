#!/usr/bin/env python

from threading import Thread

from read_conf.zmq_listener import Getter
from event_loop.event_loop import EventLoop

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class SNMP(Getter):
    """SNMP collector class."""
    def __init__(self):
        super().__init__()

    def main(self):
        """Start a thread to getting the snmp configuration and start SNMP collector."""
        thread_ = Thread(target=self.always_listen, args=('REP',))
        thread_.daemon = True
        thread_.start()

        EventLoop().run_forever()

        thread_.join()


if __name__ == "__main__":
    print('SNMP Begins')

    try:
        SNMP().main()

    except KeyboardInterrupt:
        import sys
        sys.exit(0)
