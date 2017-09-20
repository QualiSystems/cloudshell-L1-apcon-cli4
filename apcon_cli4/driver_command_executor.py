#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.layer_one.core.command_executor import CommandExecutor
from apcon_cli4.driver_commands import DriverCommands


class DriverCommandExecutor(CommandExecutor):
    """
    Mrv command executor
    """

    def __init__(self, logger):
        super(DriverCommandExecutor, self).__init__(logger)
        self._driver_instance = DriverCommands(logger)

    def driver_instance(self):
        """
        Instance of the driver commands
        :return:
        :rtype: apcon_cli4.DriverCommands
        """
        return self._driver_instance
