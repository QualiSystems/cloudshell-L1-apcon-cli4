#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from collections import defaultdict

import apcon_cli4.command_templates.autoload as command_template
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class AutoloadActions(object):
    """
    Autoload actions
    """

    def __init__(self, cli_service, logger):
        """
        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def chassis_table(self):
        """
        Chassis table
        :return:
        """
        output = CommandTemplateExecutor(self._cli_service, command_template.CHASSIS_INFO).execute_command()
        chassis_table = {}
        for line in output.split('\n'):
            if line.strip():
                name, value = line.split(':', 1)
                chassis_table[name.strip()] = value.strip()
        return chassis_table

    def slot_table(self):
        """
        Slot table
        :return:
        """
        output = CommandTemplateExecutor(self._cli_service, command_template.BLADE_INFO).execute_command()
        blade_table = defaultdict(dict)
        for line in output.split('\n'):
            if line.strip():
                key, value = line.split(':', 1)
                match = re.search(r'Blade\s(?P<letter>[A-Z])\s(?P<name>.+)', key)
                if match:
                    blade_table[match.group('letter').strip()][match.group('name').strip()] = value.strip()
        return blade_table

    def port_table(self):
        """
        Port table
        :return:
        """
        output = CommandTemplateExecutor(self._cli_service, command_template.PORT_INFO).execute_command()
        result = self._parse_table(output)
        return result

    def mapping_info(self):
        """
        Protocol table
        :return: 
        """
        output = CommandTemplateExecutor(self._cli_service, command_template.MAPPING_INFO).execute_command()
        result = self._parse_table(output)
        return result

