import time
from homeassistant.components.sensor import SensorEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import (
    BUTTON,
    BUTTON_BOTH,
    CUBE,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
    PROP_TO_ATTR_BASE,
    VIBRATION
)

TYPE = "sensor"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "action": AiotActionSensor,
        "default": AiotSensorEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotSensorEntity(AiotEntityBase, SensorEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_state_class = kwargs.get("state_class")
        self._attr_name = f"{self._attr_name} {self._attr_device_class}"
        self._attr_native_unit_of_measurement = kwargs.get("unit_of_measurement")

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "battry":
            return int(res_value)
        if res_name == "energy":
            return round(float(res_value) / 1000.0, 3)
        if res_name == "temperature":
            return round(int(res_value) / 100.0, 1)
        if res_name == "humidity":
            return round(int(res_value) / 100.0,1)
        return super().convert_res_to_attr(res_name, res_value)




class AiotActionSensor(AiotSensorEntity, SensorEntity):
    @property
    def icon(self):
        return 'mdi:bell'

    @property
    def extra_state_attributes(self):
        """Return the optional state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR_BASE.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        return data

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_value != 0 and res_value != "" and res_name == "button":
            if res_name == 'vibration' and res_value != '2':
                click_type = VIBRATION.get(res_value, 'unkown')
            if "button" in res_name:
                click_type = BUTTON.get(res_value, 'unkown')

            self.schedule_update_ha_state()
            return click_type
        return super().convert_res_to_attr(res_name, res_value)