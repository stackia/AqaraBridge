from homeassistant.components.climate import TEMP_CELSIUS
from homeassistant.components.light import (
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_COLOR_TEMP,
)
from homeassistant.components.cover import (
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_SET_POSITION,
    SUPPORT_STOP,
)
from homeassistant.components.climate import (
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
)
from homeassistant.components.remote import SUPPORT_LEARN_COMMAND
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_MOTION
)
from homeassistant.const import (
    # ATTR_BATTERY_LEVEL,
    # ATTR_TEMPERATURE,
    CONDUCTIVITY,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_CO2,
    ENERGY_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    LIGHT_LUX,
    PERCENTAGE,
    POWER_WATT,
    PRESSURE_HPA,
    TEMP_CELSIUS,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    STATE_OPEN,
    STATE_OPENING,
    # STATE_CLOSED,
    STATE_CLOSING,
    STATE_LOCKED,
    STATE_UNLOCKED
    )

try:
    from homeassistant.const import DEVICE_CLASS_GAS
except:
    DEVICE_CLASS_GAS = "gas"
try:
    from homeassistant.const import DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS
except:
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"

# AiotDevice Mapping
MK_MAPPING_PARAMS = "mapping_params"
MK_INIT_PARAMS = "init_params"
MK_RESOURCES = "resources"
MK_HASS_NAME = "hass_attr_name"

AIOT_DEVICE_MAPPING = [{
    # Aqara M1S网关
    'lumi.gateway.acn01': ["Aqara", "Gateway M1S", "ZHWG15LM"],
    'lumi.gateway.acn004': ["Aqara", "Gateway M1S 22", "ZHWG15LM"],
    'params': [
        {
            "light": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "light",
                    "supported_features": SUPPORT_BRIGHTNESS | SUPPORT_COLOR,
                    "color_mode": "hs",
                },
                MK_RESOURCES: {
                    "toggle": ("14.7.111", "_attr_is_on"),
                    "color": ("14.7.85", "_attr_hs_color"),
                    "brightness": ("14.7.1006", "_attr_brightness"),
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "illuminance",
                    "device_class": DEVICE_CLASS_ILLUMINANCE,
                    "state_class": "measurement",
                    "unit_of_measurement": LIGHT_LUX
                },
                MK_RESOURCES: {"illumination": ("0.3.85", "_attr_native_value")},
            }
        }
    ]
}, {
    'lumi.gateway.sacn01': ["Aqara", "Smart Hub H1", "QBCZWG11LM"],
    'params': [
    ]
}, {
    'lumi.gateway.aqcn02': ["Aqara", "Hub E1", "ZHWG16LM"],
    'params': []
}, {
    'lumi.ctrl_neutral1.v1': ["Aqara", "Single Wall Switch", "QBKG04LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "disable_btn":("4.10.85","_attr_disable_btn"),
                }
            }
        }
    ]
}, {
    # 墙壁开关（单火线单键版） 
    'lumi.ctrl_neutral1.v1': ["Aqara", "Wall Switch (Single Rocker)", "QBKG04LM"],
    # 智能墙壁开关H1（单火线单键版）
    'lumi.switch.l1acn1':["Aqara", "Wall Switch H1 (Single Rocker)", "QBKG27LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "disable_btn":("4.10.85","_attr_disable_btn"),
                }
            }
        }
    ]
}, {
    # 智能墙壁开关H1（单火线双键版）
    'lumi.switch.l2acn1':["Aqara", "Wall Switch H1 (Double Rocker)", "QBKG28LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.{}.85", "_attr_is_on"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    # "disable_btn":("4.1{}.85","_attr_disable_btn"), 对应不上无法处理数据，async_set_attr，get_res_id_by_name
                },
                MK_MAPPING_PARAMS: {"ch_count": 2},
            }
        }
    ]
}, {
    # 智能墙壁开关H1（单火线三键版）
    'lumi.switch.l3acn1':["Aqara", "Wall Switch H1 (Three Rocker)", "QBKG29LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch",
                },
                MK_RESOURCES: {
                    "toggle": ("4.{}.85", "_attr_is_on"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    # "disable_btn":("4.1{}.85","_attr_disable_btn"), 对应不上无法处理数据，async_set_attr，get_res_id_by_name
                },
                MK_MAPPING_PARAMS: {"ch_count": 3},
            }
        }
    ]
}, {
    # temperature and humidity sensor
    'lumi.sensor_ht.v1': ["Xiaomi", "TH Sensor", "WSDCGQ01LM"],
    'params': [
        {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "temperature",
                    "device_class": DEVICE_CLASS_TEMPERATURE,
                    "state_class": "measurement",
                    "unit_of_measurement": TEMP_CELSIUS
                },
                MK_RESOURCES: {"temperature": ("0.1.85", "_attr_native_value")},
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "humidity",
                    "device_class": DEVICE_CLASS_HUMIDITY,
                    "state_class": "measurement",
                    "unit_of_measurement": PERCENTAGE
                },
                MK_RESOURCES: {"humidity": ("0.2.85", "_attr_native_value")},
            }
        }
    ]
},
]

SPECIAL_DEVICES_INFO = {
    # VRF空调控制器
    "lumi.airrtc.vrfegl01": {
        "toggle": {0: "on", 1: "off"},
        "hvac_mode": {
            0: "heat",
            1: "cool",
            2: "auto",
            3: "dry",
            4: "fan_only",
        },
        "fan_mode": {0: "low", 1: "middle", 2: "high", 3: "auto"},
        "swing_mode": {0: "horizontal", 1: "vertical", 2: "both"},
        "swing_toggle": {1: "off"},
    }
}
