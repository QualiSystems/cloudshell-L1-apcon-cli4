#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict()
ERROR_MAP = OrderedDict(
    [(r'[Ee]rror:', 'Mapping error, Hardware incompatibility')])

MAP_BIDI = CommandTemplate('connect duplex {src_port}{dst_port}', ACTION_MAP, ERROR_MAP)
MAP_UNI = CommandTemplate('connect aggregation {src_port} {dst_port}', ACTION_MAP, ERROR_MAP)
MAP_TAP = CommandTemplate('connect aggregation duplex {src_port} {dst_port} {tap_port}', ACTION_MAP, ERROR_MAP)
MAP_CLEAR = CommandTemplate('disconnect {port}', ACTION_MAP, ERROR_MAP)
GET_CURRENT_CONNECTIONS = CommandTemplate('show connections raw', ACTION_MAP, ERROR_MAP)
