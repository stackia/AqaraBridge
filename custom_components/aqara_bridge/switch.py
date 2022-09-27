from homeassistant.components.switch import SwitchEntity

from .core.aiot_manager import AiotManager, AiotToggleableEntityBase
from .core.const import DOMAIN, HASS_DATA_AIOT_MANAGER, PROP_TO_ATTR_BASE

TYPE = "switch"

ATTR_IN_USE = "in_use"
ATTR_DISABLE_BTN = "disable_btn"

PROP_TO_ATTR = {
    "in_use": ATTR_IN_USE,
    "disable_btn": ATTR_DISABLE_BTN
}

DATA_KEY = f"{TYPE}.{DOMAIN}"

async def async_setup_entry(hass, config_entry, async_add_entities):
    manager: AiotManager = hass.data[DOMAIN][HASS_DATA_AIOT_MANAGER]
    cls_entities = {
        "default": AiotSwitchEntity
    }
    await manager.async_add_entities(
        config_entry, TYPE, cls_entities, async_add_entities
    )


class AiotSwitchEntity(AiotToggleableEntityBase, SwitchEntity):
    _attr_in_use = None
    _attr_disable_btn = None

    def __init__(self, hass, device, res_params, channel=None, **kwargs):
        AiotToggleableEntityBase.__init__(
            self, hass, device, res_params, TYPE, channel, **kwargs
        )

    @property
    def icon(self):
        """return icon."""
        return 'mdi:power-socket'

    @property
    def in_use(self):
        """Return the plug detection."""
        return self._attr_in_use
    
    @property
    def disable_btn(self):
        """Return the button physical control."""
        return self._attr_disable_btn


    @property
    def extra_state_attributes(self):
        """Return the optional state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR_BASE.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        for prop, attr in PROP_TO_ATTR.items():
            value = getattr(self, prop)
            if value is not None:
                data[attr] = value

        return data

    def convert_res_to_attr(self, res_name, res_value):
        if res_name == "toggle" or res_name == "decoupled":
            return res_value == "1"
        if res_name == "energy":
            return round(float(res_value) / 1000.0, 3)
        if res_name == "chip_temperature":
            return round(float(res_value), 1)
        if res_name == "fw_ver":
            return res_value
        if res_name == "lqi":
            return int(res_value)
        if res_name == "in_use":
            return res_value == "1"
        return super().convert_res_to_attr(res_name, res_value)
