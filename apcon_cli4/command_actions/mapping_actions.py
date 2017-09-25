#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

import apcon_cli4.command_templates.mapping as command_template
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class MappingActions(object):
    def __init__(self, cli_service, logger):
        """
        Mapping actions
        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """

        self._cli_service = cli_service
        self._logger = logger

    def map_bidi(self, src_port, dst_port):
        """
        Bidirectional mapping
        :param src_port: 
        :param dst_port: 
        :return: 
        """

        output = CommandTemplateExecutor(self._cli_service, command_template.MAP_BIDI).execute_command(
            src_port=src_port, dst_port=dst_port)
        return output

    def map_uni(self, src_port, dst_port):
        """
        Unidirectional mapping
        :param src_port: 
        :param dst_port: 
        :return:
        """

        output = CommandTemplateExecutor(self._cli_service, command_template.MAP_UNI).execute_command(
            src_port=src_port, dst_port=dst_port)
        return output

    def map_tap(self, src_port, dst_port):
        bidi_dst_port = None
        output = ""
        current_config = CommandTemplateExecutor(self._cli_service,
                                                 command_template.GET_CURRENT_CONNECTIONS).execute_command()
        if src_port in current_config:

            for line in current_config.splitlines():
                if src_port in line:
                    ports = re.findall(r"[A-Z]\d+", line)
                    bidi_dst_port = ports[0]
                    break
        if bidi_dst_port:
            self.map_clear_to(src_port)
            output = CommandTemplateExecutor(self._cli_service, command_template.MAP_TAP).execute_command(
                src_port=src_port, dst_port=bidi_dst_port, tap_port=dst_port)
        return output

    def map_clear(self, ports):
        """
        Clear bidirectional mapping
        :param ports: 
        :return: 
        """

        output = ""
        executor = CommandTemplateExecutor(self._cli_service, command_template.MAP_CLEAR)
        for port in ports:
            output += executor.execute_command(port=port)
        return output

    def map_clear_to(self, src_port):
        """
        Clear unidirectional mapping
        :param src_port: 
        :return:
        """

        output = CommandTemplateExecutor(self._cli_service, command_template.MAP_CLEAR).execute_command(
            src_port=src_port)
        return output
