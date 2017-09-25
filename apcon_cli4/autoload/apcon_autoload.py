from apcon_cli4.autoload.resource_description import ResourceDescription
from apcon_cli4.command_actions.autoload_actions import AutoloadActions
from cloudshell.layer_one.core.response.response_info import ResourceDescriptionResponseInfo


class ApconAutoload(object):
    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger
        self._autoload_actions = AutoloadActions(cli_handler, self._logger)
        self.__chassis_table = None
        self.__slot_table = None
        self.__port_table = None
        self.__port_protocol_table = None

    @property
    def _chassis_table(self):
        if not self.__chassis_table:
            self.__chassis_table = self._autoload_actions.chassis_table()
        return self.__chassis_table

    @property
    def _slot_table(self):
        if not self.__slot_table:
            self.__slot_table = self._autoload_actions.slot_table()
        return self.__slot_table

    @property
    def _port_table(self):
        if not self.__port_table:
            self.__port_table = self._autoload_actions.port_table()
        return self.__port_table

    def discover_device(self, address):
        response_info = ResourceDescriptionResponseInfo(
            ResourceDescription(address, self._chassis_table, self._slot_table, self._port_table).build())
        return response_info


if __name__ == "__main__":
    from apcon_cli4.cli.apcon_cli_handler import ApconCliHandler
    from cloudshell.core.logger.qs_logger import get_qs_logger

    logger = get_qs_logger()
    cli_handler = ApconCliHandler(logger)
    cli_handler.define_session_attributes("192.168.41.47", "admin", "secret")
    with cli_handler.default_mode_service() as session:
        autoload = ApconAutoload(session, logger)
        autoload.discover_device("192.168.41.47")
