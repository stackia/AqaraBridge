""" the Aqara Bridge utils."""
import logging
import re
import uuid
import tzlocal
from datetime import datetime
from aiohttp import web

from homeassistant.core import HomeAssistant
from homeassistant.util.dt import DEFAULT_TIME_ZONE, get_time_zone
from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers.typing import HomeAssistantType

def local_zone(hass=None):
    try:
        if isinstance(hass, HomeAssistant):
            return get_time_zone(hass.config.time_zone)
        return tzlocal.get_localzone()
    except KeyError:
        pass
    return DEFAULT_TIME_ZONE
