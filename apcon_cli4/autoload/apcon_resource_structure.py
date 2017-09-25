import re
from cloudshell.layer_one.core.response.resource_info.entities.attributes import StringAttribute, NumericAttribute, \
    BooleanAttribute


class ApconAttributes(object):
    """
    Apcon Attributes
    """

    def __init__(self, resource_table, defined_attributes):
        self._resource_table = resource_table
        self._defined_attributes = defined_attributes

    def get_attribute(self, attribute_name, address):
        """
        Attribute by name
        :param attribute_name: 
        :param address: 
        :return:
        :rtype: cloudshell.layer_one.core.response.resource_info.entities.base.Attribute
        """
        if attribute_name in self._defined_attributes:
            return self._defined_attributes[attribute_name](address)
        raise Exception(self.__class__.__name__, 'Attribute {} is not defined'.format(attribute_name))

    def get_attributes(self, address):
        attributes = []
        for attribute_name in self._defined_attributes:
            attribute = self.get_attribute(attribute_name, address)
            if attribute.value != attribute.DEFAULT_VALUE:
                attributes.append(attribute)
        return attributes


class ApconChassisAttributes(ApconAttributes):
    MODEL_NAME = 'Model Name'
    SERIAL_NUMBER = 'Serial Number'
    OS_VERSION = 'OS Version'

    def __init__(self, resource_table):
        super(ApconChassisAttributes, self).__init__(resource_table, {self.MODEL_NAME: self.model_name,
                                                                      self.SERIAL_NUMBER: self.serial_number,
                                                                      self.OS_VERSION: self.os_version})

    def model_name(self, address):
        value = self._resource_table.get(address).get('model')
        return StringAttribute(self.MODEL_NAME, value or StringAttribute.DEFAULT_VALUE)

    def serial_number(self, address):
        value = self._resource_table.get(address).get('serial_number')
        return StringAttribute(self.SERIAL_NUMBER, value or StringAttribute.DEFAULT_VALUE)

    def os_version(self, address):
        value = self._resource_table.get(address).get('os_version')
        return StringAttribute(self.SERIAL_NUMBER, value or StringAttribute.DEFAULT_VALUE)


class ApconSlotAttributes(ApconAttributes):
    MODEL_NAME = 'Model Name'
    SERIAL_NUMBER = 'Serial Number'

    def __init__(self, resource_table):
        super(ApconSlotAttributes, self).__init__(resource_table, {self.MODEL_NAME: self.model_name,
                                                                   self.SERIAL_NUMBER: self.serial_number})

    def model_name(self, address):
        value = self._resource_table.get(address).get('model')
        return StringAttribute(self.MODEL_NAME, value or StringAttribute.DEFAULT_VALUE)

    def serial_number(self, address):
        value = self._resource_table.get(address).get('serail_number')
        return StringAttribute(self.SERIAL_NUMBER, value or StringAttribute.DEFAULT_VALUE)


class ApconPortAttributes(ApconAttributes):
    MODEL_NAME = 'Model Name'
    PROTOCOL_VALUE = 'Protocol Value'
    PROTOCOL_TYPE_VALUE = 'Protocol Type Value'
    DUPLEX = 'Duplex'
    AUTO_NEGOTIATION = 'Auto Negotiation'
    RX_POWER = 'Rx Power (dBm)'
    TX_POWER = 'Tx Power (dBm)'
    WAVELENGTH = 'Wavelength'
    PORT_SPEED = 'Port Speed'

    def __init__(self, resource_table):
        super(ApconPortAttributes, self).__init__(resource_table, {self.MODEL_NAME: self.model_name,
                                                                   self.PROTOCOL_VALUE: self.protocol_value,
                                                                   self.PROTOCOL_TYPE_VALUE: self.protocol_type_value,
                                                                   self.DUPLEX: self.duplex,
                                                                   self.AUTO_NEGOTIATION: self.auto_negotiation,
                                                                   self.PORT_SPEED: self.port_speed})

    def model_name(self, address):
        value = self._resource_table.get(address).get('model')
        return StringAttribute(self.MODEL_NAME, value or StringAttribute.DEFAULT_VALUE)

    def protocol_value(self, address):
        value = self._resource_table.get(address).get('protocol')
        return StringAttribute(self.PROTOCOL_VALUE, value or StringAttribute.DEFAULT_VALUE)

    def protocol_type_value(self, address):
        value = self._resource_table.get(address).get('protocol_type')
        return StringAttribute(self.PROTOCOL_TYPE_VALUE, value or StringAttribute.DEFAULT_VALUE)

    def duplex(self, address):
        value = self._resource_table.get(address).get('duplex')
        if re.match(r'full', value, flags=re.IGNORECASE):
            num_value = '3'
        elif re.match(r'half', value, flags=re.IGNORECASE):
            num_value = '2'
        else:
            num_value = NumericAttribute.DEFAULT_VALUE

        return NumericAttribute(self.DUPLEX, num_value)

    def auto_negotiation(self, address):
        out = self._resource_table.get(address).get('autoneg')
        if re.match(r'on|true', out, flags=re.IGNORECASE):
            value = BooleanAttribute.TRUE
        else:
            value = BooleanAttribute.FALSE
        return BooleanAttribute(self.AUTO_NEGOTIATION, value or BooleanAttribute.DEFAULT_VALUE)

    def rx_power(self, address):
        value = self._resource_table.get(address).get('rx_signal')
        return StringAttribute(self.RX_POWER, value or StringAttribute.DEFAULT_VALUE)

    def tx_power(self, address):
        value = self._resource_table.get(address).get('tx_signal')
        return StringAttribute(self.TX_POWER, value or StringAttribute.DEFAULT_VALUE)

    def port_speed(self, address):
        value = self._resource_table.get(address).get('speed')
        return StringAttribute(self.PORT_SPEED, value or StringAttribute.DEFAULT_VALUE)

    def wavelength(self, address):
        value = self._resource_table.get(address).get('wavelength')
        return StringAttribute(self.WAVELENGTH, value or StringAttribute.DEFAULT_VALUE)
