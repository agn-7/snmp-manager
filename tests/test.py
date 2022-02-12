import pytest

from snmp_collector.event_loop import EventLoop


class TestCase:
    @pytest.mark.parametrize("test_case", [])
    def test_events(self, test_case):
        assert EventLoop().run_once()
