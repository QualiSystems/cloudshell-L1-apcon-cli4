#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

from cloudshell.core.logger.qs_logger import get_qs_logger
from cloudshell.layer_one.core.driver_listener import DriverListener
from cloudshell.layer_one.core.helper.runtime_configuration import RuntimeConfiguration
from cloudshell.layer_one.core.helper.xml_logger import XMLLogger
from apcon_cli4.driver_command_executor import DriverCommandExecutor

if __name__ == '__main__':
    driver_name = 'APCON_CLI4'

    # Determining log path
    driver_path = os.path.dirname(sys.argv[0])
    log_path = os.path.join(driver_path, '..', 'Logs')
    os.environ['LOG_PATH'] = log_path

    # Reading runtime configuration
    runtime_config = RuntimeConfiguration(
        os.path.join(driver_path, driver_name + '_' + 'RuntimeConfig.yml'))

    # Creating XMl logger instance
    xml_file_name = driver_name + '--' + datetime.now().strftime('%d-%b-%Y--%H-%M-%S') + '.xml'
    xml_logger = XMLLogger(os.path.join(log_path, driver_name, xml_file_name))

    # Creating command logger instance
    command_logger = get_qs_logger(log_group=driver_name,
                                   log_file_prefix=driver_name + '_commands', log_category='COMMANDS')
    log_level = runtime_config.read_key('LOGGING.LEVEL')
    print log_level
    if log_level:
        command_logger.setLevel(log_level)

    command_logger.debug('Starting driver {}'.format(driver_name))

    # Creating command executor instance
    command_executor = DriverCommandExecutor(command_logger)

    # Creating listener instance
    server = DriverListener(command_executor, xml_logger, command_logger)

    # Start listening socket
    server.start_listening(port=sys.argv[1] if len(sys.argv) > 1 else None)