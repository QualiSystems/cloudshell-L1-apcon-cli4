#!/usr/bin/python
# -*- coding: utf-8 -*-
from apcon_cli4.autoload.apcon_resource_structure import ApconChassisAttributes, ApconSlotAttributes, \
    ApconPortAttributes
from apcon_cli4.helpers.address import Address

from cloudshell.layer_one.core.response.resource_info.entities.blade import Blade
from cloudshell.layer_one.core.response.resource_info.entities.chassis import Chassis
from cloudshell.layer_one.core.response.resource_info.entities.port import Port


class ResourceDescription(object):
    """Apcon resource description builder"""

    def __init__(self, address, chassis_table, slot_table, port_table):
        self._resource_address = address
        self._chassis_table = chassis_table
        self._slot_table = slot_table
        self._port_table = port_table

        self._mapping_table = {}

    # Build Chassis
    def _build_chassis(self):
        chassis_dict = {}
        chassis_attributes = ApconChassisAttributes(self._chassis_table)
        for address, record in self._chassis_table.iteritems():
            model_name = 'Generic Apcon Chassis'
            serial_number = chassis_attributes.serial_number(address).value
            chassis = Chassis(address.index(), self._resource_address, model_name, serial_number)
            chassis.attributes = chassis_attributes.get_attributes(address)
            chassis_dict[address] = chassis
        return chassis_dict

    # Build blades
    def _build_blades(self, chassis_dict):
        blades_dict = {}
        slots_attributes = ApconSlotAttributes(self._slot_table)
        for address, record in self._slot_table.iteritems():
            model_name = 'Generic L1 Module'
            blade_model = slots_attributes.model_name(address).value
            serial_number = slots_attributes.serial_number(address).value
            blade_address = Address(0, address)

            chassis_address = blade_address.get_chassis_address()
            try:
                chassis = chassis_dict[chassis_address]
            except KeyError:
                raise Exception(
                    'Fail to get information for the Chassis {}'.format(chassis_address))

            blade = Blade(blade_address.index(), model_name, serial_number)
            blade.attributes = slots_attributes.get_attributes(address)
            blades_dict[blade_address] = blade
            blade.set_parent_resource(chassis)
        return blades_dict

    def _build_ports(self, blades_dict):
        ports_dict = {}
        ports_attributes = ApconPortAttributes(self._port_table)
        for address, record in self._port_table.iteritems():
            blade = blades_dict.get(address.get_slot_address())
            if blade:
                serial_number = record.get('serial_number')
                model_name = 'Generic L1 Port'
                port = Port(address.index(), model_name, serial_number)
                port.attributes = ports_attributes.get_attributes(address)
                ports_dict[address] = port
                port_mapping_address = record.get("mapped_to")
                if port_mapping_address:
                    self._mapping_table[address] = port_mapping_address
                port.set_parent_resource(blade)
        return ports_dict

    # Mappings
    def _build_ports_mappings(self, ports_dict):
        for src_address, dst_address in self._mapping_table.iteritems():
            src_port = ports_dict.get(src_address)
            dst_port = ports_dict.get(dst_address)
            src_port.add_mapping(dst_port)

    def build(self):
        chassis_dict = self._build_chassis()
        blades_dict = self._build_blades(chassis_dict)
        ports_dict = self._build_ports(blades_dict)
        self._build_ports_mappings(ports_dict)
        return chassis_dict.values()
