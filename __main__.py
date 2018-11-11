#!/usr/bin/env python

from threading import Thread

from zmq_listener import Getter
from event_loop import EventLoop

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class SNMP(Getter):
    def __init__(self):
        super().__init__()

    def main(self):
        # thread_ = Thread(target=self.listen)
        thread_ = Thread(target=self.always_listen, args=('SUB',))
        thread_.daemon = True
        # thread_.start()  # TODO

        EventLoop().run_forever()

        # thread_.join()  # TODO


if __name__ == "__main__":
    print('Start')

    try:
        SNMP().main()

    except KeyboardInterrupt:
        pass
