#!/usr/bin/python
# -*- coding: utf-8 -*-
from apcon_cli4.autoload.apcon_autoload import ApconAutoload
from apcon_cli4.cli.apcon_cli_handler import ApconCliHandler
from apcon_cli4.command_actions.mapping_actions import MappingActions
from apcon_cli4.command_actions.system_actions import SystemActions
from cloudshell.layer_one.core.driver_commands_interface import DriverCommandsInterface
from cloudshell.layer_one.core.response.response_info import GetStateIdResponseInfo


class DriverCommands(DriverCommandsInterface):
    """
    Driver commands implementation
    """

    def __init__(self, logger):
        """
        :param logger: 
        """

        self._logger = logger
        self._cli_handler = ApconCliHandler(self._logger)

    def get_state_id(self):
        return GetStateIdResponseInfo("-1")

    def set_state_id(self, state_id):
        pass

    def map_bidi(self, src_port, dst_port):
        with self._cli_handler.default_mode_service() as session:
            _mapping_actions = MappingActions(session, self._logger)
            _mapping_actions.map_bidi(src_port, dst_port)

    def map_uni(self, src_port, dst_port):
        with self._cli_handler.default_mode_service() as session:
            _mapping_actions = MappingActions(session, self._logger)
            _mapping_actions.map_uni(src_port, dst_port)

    def get_resource_description(self, address):
        with self._cli_handler.default_mode_service() as session:
            apcon_autoload = ApconAutoload(session, self._logger)
            return apcon_autoload.discover_device(address)

    def map_clear(self, ports):
        with self._cli_handler.default_mode_service() as session:
            _mapping_actions = MappingActions(session, self._logger)
            _mapping_actions.map_clear(ports)

    def login(self, address, username, password):
        self._cli_handler.define_session_attributes(address, username, password)
        with self._cli_handler.default_mode_service() as session:
            system_actions = SystemActions(session, self._logger)
            self._logger.info(system_actions.device_info())

    def map_clear_to(self, src_port, dst_port):
        with self._cli_handler.default_mode_service() as session:
            _mapping_actions = MappingActions(session, self._logger)
            _mapping_actions.map_clear_to(src_port)

    def get_attribute_value(self, cs_address, attribute_name):
        pass

    def set_attribute_value(self, cs_address, attribute_name, attribute_value):
        pass

    def map_tap(self, src_port, dst_port):
        pass
