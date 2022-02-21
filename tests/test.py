import pytest
import asyncio

from interruptingcow import timeout

from snmp_collector.event_loop import EventLoop


class TestCase:
    @pytest.mark.timeout(10)
    def endless(self):
        EventLoop().run_forever()

    @pytest.mark.parametrize("test_case", ['none'])
    def test_events(self, test_case: list):
        assert EventLoop().run_once()

    @pytest.mark.parametrize("test_case", ['none'])
    def test_events2(self, test_case: list):
        try:
            with timeout(10, exception=asyncio.CancelledError):
                EventLoop().run_forever()
                assert False
        except:
            assert True

if __name__ == "__main__":
    assert EventLoop().run_once()
    try:
        with timeout(5, exception=asyncio.CancelledError):
            EventLoop().run_forever()
            assert False
    except:
        assert True
