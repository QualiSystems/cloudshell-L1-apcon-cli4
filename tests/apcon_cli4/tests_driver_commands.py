from unittest import TestCase
from apcon_cli4.driver_commands import DriverCommands
from mock import MagicMock


class DriverCommandsTests(TestCase):
    def setUp(self):
        self.driver = DriverCommands(MagicMock())

    def test_get_resource_id(self):
        result = self.driver.get_state_id()
        print result
