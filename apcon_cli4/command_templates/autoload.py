#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict()
ERROR_MAP = OrderedDict([(r'[Ee]rror:', 'Command error')])

CHASSIS_INFO = CommandTemplate('show switch info', ACTION_MAP, ERROR_MAP)
BLADE_INFO = CommandTemplate('show blade info raw *', ACTION_MAP, ERROR_MAP)
PORT_INFO = CommandTemplate('show port info *', ACTION_MAP, ERROR_MAP)
MAPPING_INFO = CommandTemplate('show connections simple', ACTION_MAP, ERROR_MAP)

