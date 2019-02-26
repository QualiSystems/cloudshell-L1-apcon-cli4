#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from collections import defaultdict

import apcon_cli4.command_templates.autoload as command_template
from apcon_cli4.helpers.address import Address
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
        chassis_table_match = re.search(
            r"switch\s+name:\s+(?P<name>\S+)\s+"
            r"switch\s+model:\s+(?P<model>\S+).*"
            r"switch\s+serial\s+number:\s+(?P<serial_number>\S+)\s+.*"
            r"(controller|cntrl)\s+software:\s+(?P<os_version>\S+)\s+",
            output,
            flags=(re.DOTALL + re.IGNORECASE)
        )
        if chassis_table_match:
            chassis_table[Address(0)] = chassis_table_match.groupdict()
        return chassis_table

    def slot_table(self):
        """
        Slot table
        :return:
        """

        output = CommandTemplateExecutor(self._cli_service, command_template.BLADE_INFO).execute_command()
        blade_table = defaultdict(dict)
        for line in output.split('\n'):
            if line.strip() and ("model" in line.lower() or "serial" in line.lower()):
                if "model" in line.lower():
                    key, value = re.split(":\s+", line)
                    match = re.search(r'Blade\s(?P<letter>[A-Z])\s(?P<name>\S+)', key)
                    if match:
                        blade_table[match.group('letter').strip()][match.group('name').strip()] = value.strip()
        return blade_table

    def port_table(self):
        """
        Port table
        :return:
        """

        map_types_dict = {">>": "uni", "<>": "bidi"}
        port_dict = dict()
        output = CommandTemplateExecutor(self._cli_service, command_template.PORT_NAMES).execute_command()
        port_list = re.findall(r"[A-Z]\d+", output)
        for port in port_list:
            port_info_dict = dict()
            port_info_dict["speed"] = ""
            port_info_dict["serial_number"] = ""
            port_info_dict["autoneg"] = ""
            port_info_dict["protocol"] = ""
            port_info_dict["protocol_type"] = ""
            port_info_dict["wavelength"] = ""
            port_info_dict["duplex"] = ""
            port_info_dict["rx_signal"] = ""
            port_info_dict["tx_signal"] = ""
            port_info = CommandTemplateExecutor(self._cli_service,
                                                      command_template.PORT_INFO).execute_command(port_name=port)
            for port_info_line in port_info.splitlines():
                if "rate" in port_info_line.lower():
                    speed = port_info_line.split(":")[-1]
                    port_info_dict["speed"] = speed
                    port_info_dict["protocol_type"] = speed
                    continue

                if "protocol" in port_info_line.lower():
                    port_info_dict["protocol"] = port_info_line.split(":")[-1].strip()
                    continue

                if "wavelength" in port_info_line.lower():
                    port_info_dict["wavelength"] = port_info_line.split(":")[-1].strip()
                    continue

                if "serial" in port_info_line.lower():
                    port_info_dict["serial_number"] = port_info_line.split(":")[-1].strip()
                    continue

                if "rx signal" in port_info_line.lower():
                    port_info_dict["rx_signal"] = port_info_line.split(":")[-1].strip()
                    continue

                if "tx signal" in port_info_line.lower():
                    port_info_dict["tx_signal"] = port_info_line.split(":")[-1].strip()
                    continue

                if "autoneg" in port_info_line.lower():
                    port_info_dict["autoneg"] = port_info_line.split(":")[-1].strip()
                    continue

                if "connections" in port_info_line.lower():
                    # A31 Incoming_mapping = A15
                    # A15 Incoming mapping = A20
                    # A20 Incoming mapping = A15
                    map_info = port_info_line.split(":")[-1].strip()
                    if map_info and port in map_info:
                        map_type = map_types_dict.get(map_info.split()[1])
                        if map_type:
                            if map_info.split()[-1] == port:
                                incoming_port_id = map_info.split()[0]
                            else:
                                incoming_port_id = map_info.split()[-1]
                            incoming_port = Address(0, map_info.split()[-1][:1], incoming_port_id)
                            port_info_dict["mapped_to"] = incoming_port

            port_dict[Address(0, port[:1], port)] = port_info_dict
        return port_dict
