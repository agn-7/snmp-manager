import pytest

from snmp_collector.event_loop import EventLoop


class TestCase:
    @pytest.mark.parametrize("test_case", ['none'])
    def test_events(self, test_case):
        assert EventLoop().run_once()


if __name__ == "__main__":
    assert EventLoop().run_once()
