"""Support for Xiaomi Aqara binary sensors."""
import time

from homeassistant.config import DATA_CUSTOMIZE
from homeassistant.helpers.event import async_call_later
from homeassistant.components.binary_sensor import BinarySensorEntity

from .core.aiot_manager import (
    AiotManager,
    AiotEntityBase,
)
from .core.const import (
    CONF_OCCUPANCY_TIMEOUT,
    DOMAIN,
    HASS_DATA_AIOT_MANAGER,
    PROP_TO_ATTR_BASE
)

TYPE = "binary_sensor"

DATA_KEY = f"{TYPE}.{DOMAIN}"


async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "motion": AiotMotionBinarySensor,
        "contact": AiotDoorBinarySensor,
        "default": AiotBinarySensorEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotBinarySensorEntity(AiotEntityBase, BinarySensorEntity):
    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotEntityBase.__init__(self, hass, device, res_params, TYPE, channel, **kwargs)
        self._attr_state_class = kwargs.get("state_class")
        self._attr_name = f"{self._attr_name} {self._attr_device_class}"
        self._extra_state_attributes.extend(["trigger_time", "trigger_dt"])

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "firmware_version":
            return res_value
        if res_name == "zigbee_lqi":
            return int(res_value)
        if res_name == "voltage":
            return format(float(res_value) / 1000, '.3f')
        if res_name in ["moisture", "smoke"]:
            return int(res_value) != 0
        return super().convert_res_to_attr(res_name, res_value)

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self.device_class in ["moisture", "smoke"] and self._attr_is_on is None:
            return False
        return self._attr_is_on
        
class AiotMotionBinarySensor(AiotBinarySensorEntity, BinarySensorEntity):
    # 不需要自定义定时器，通过消息订阅
    def convert_res_to_attr(self, res_name, res_value):
        if res_name in ["firmware_version", "zigbee_lqi", "voltage"]:
            return super().convert_res_to_attr(res_name, res_value)

        self._attr_is_on = not bool(res_value)
        self.schedule_update_ha_state()
        return not bool(res_value)


class AiotDoorBinarySensor(AiotBinarySensorEntity, BinarySensorEntity):
    def convert_res_to_attr(self, res_name, res_value):
        if res_name in ["firmware_version", "zigbee_lqi", "voltage"]:
            return super().convert_res_to_attr(res_name, res_value)

        self._attr_is_on = not bool(res_value)
        self.schedule_update_ha_state()
        return not bool(res_value)
