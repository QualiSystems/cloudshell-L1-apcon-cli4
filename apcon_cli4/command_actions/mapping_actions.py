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
            src_port=src_port.split("/")[-1], dst_port=dst_port.split("/")[-1])
        return output

    def map_uni(self, src_port, dst_port):
        """
        Unidirectional mapping
        :param src_port: 
        :param dst_port: 
        :return:
        """

        tap_src_port = src_port.split("/")[-1]
        tap_dst_port = dst_port.split("/")[-1]
        bidi_dst_port = None
        current_config = CommandTemplateExecutor(self._cli_service,
                                                 command_template.GET_CURRENT_CONNECTIONS).execute_command()
        if tap_src_port in current_config:
            for line in current_config.splitlines():
                if tap_src_port in line:
                    ports = re.findall(r"[A-Z]\d+", line)
                    for prt in ports:
                        if prt != tap_src_port:
                            bidi_dst_port = prt
                    break
        if bidi_dst_port:
            output = CommandTemplateExecutor(self._cli_service, command_template.MAP_TAP).execute_command(
                src_port=tap_src_port, dst_port=bidi_dst_port, tap_port=tap_dst_port)
        else:
            output = CommandTemplateExecutor(self._cli_service, command_template.MAP_UNI).execute_command(
                src_port=src_port.split("/")[-1], dst_port=dst_port.split("/")[-1])
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
            output += executor.execute_command(port=port.split("/")[-1])
        return output

    def map_clear_to(self, src_port):
        """
        Clear unidirectional mapping
        :param src_port: 
        :return:
        """

        output = CommandTemplateExecutor(self._cli_service, command_template.MAP_CLEAR).execute_command(
            port=src_port.split("/")[-1])
        return output
