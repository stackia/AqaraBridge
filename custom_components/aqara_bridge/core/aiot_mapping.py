from homeassistant.components.light import *
from homeassistant.components.cover import *
from homeassistant.components.climate import *
from homeassistant.components.remote import *
from homeassistant.components.binary_sensor import *
from homeassistant.const import *

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
    # 墙壁开关（单火线单键版） 
    'lumi.ctrl_neutral1.v1': ["Aqara", "Wall Switch (Single Rocker)", "QBKG04LM"],
    # 智能墙壁开关H1（单火线单键版）
    'lumi.switch.l1acn1':["Aqara", "Wall Switch H1 (Single Rocker)", "QBKG27LM"],
    # 智能墙壁开关D1（单火线单键版）
    'lumi.switch.b1lacn02': ["Aqara", "Single Wall Switch D1", "QBKG21LM"],
    # 智能墙壁开关E1（单火线单键版）
    'lumi.switch.b1lc04': ["Aqara", "Single Wall Switch D1", "QBKG21LM"],
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
    # 智能插座 (国标)
    'lumi.plug.v1': ["Xiaomi", "Plug", "ZNCZ02LM"],
    # 智能墙壁插座 H1（USB版）
    'lumi.plug.sacn03': ["Aqara", "Smart Wall Outlet H1(USB)", "QBCZWG11LM"],
    'params': [
        {
            "switch": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "switch"
                },
                MK_RESOURCES: {
                    "toggle": ("4.1.85", "_attr_is_on"),
                    "power": ("0.12.85", "_attr_current_power_w"),
                    "energy": ("0.13.85", "_attr_today_energy_kwh"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    # "in_use": ("8.0.2044", "_attr_in_use")#使用状态有问题这个参数不存在，需要修改
                }
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "power",
                    "device_class": DEVICE_CLASS_POWER,
                    "state_class": "measurement",
                    "unit_of_measurement": POWER_WATT},
                MK_RESOURCES: {"power": ("0.12.85", "_attr_native_value")}
            }
        }, {
            "sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "energy",
                    "device_class": DEVICE_CLASS_ENERGY,
                    "state_class": "total_increasing",
                    "unit_of_measurement": ENERGY_KILO_WATT_HOUR},
                MK_RESOURCES: {"energy": ("0.13.85", "_attr_native_value")},
            }
        }
    ]
},
# 无意义，无法获取更新以及订阅只能通过轮训。无法作为触发使用。
# {
#     # 无线开关（贴墙式单键版）
#     'lumi.remote.b186acn01': ["Aqara", "Single Wall Button", "WXKG03LM"],
#     # 无线开关H1（贴墙式单键版）
#     'lumi.remote.b18ac1': ["Aqara", "Wireless Remote Switch H1 (Single Rocker)", "WXKG14LM"],
#     # 无线开关E1（贴墙式单键版）
#     'lumi.remote.acn004': ["Aqara", "Wireless Remote Switch E1 (Single Rocker)", "WXKG16LM"],
#     # 无线开关D1（贴墙式单键版）
#     'lumi.remote.b186acn02': ["Aqara", "Wireless Remote Switch D1 (Single Rocker)", "WXKG06LM"],
#     # 无线开关E1 mini
#     'lumi.remote.acn007': ["Aqara", "Single Wall Button E1", "WXKG16LM"],
#     'params': [
#         {
#             "sensor": {
#                 MK_INIT_PARAMS: {
#                     MK_HASS_NAME: "action",
#                     "device_class": "",
#                     "state_class": "",
#                     "unit_of_measurement": ""
#                 },
#                 MK_RESOURCES: {"button": ("13.1.85", "_attr_native_value")},
#             }
#         }
#     ]
# }, {
#     # 无线开关（贴墙式双键版）
#     'lumi.remote.b286acn01': ["Aqara", "Double Wall Button", "WXKG02LM"],
#     # 无线开关H1（贴墙式双键版）
#     'lumi.remote.b28ac1': ["Aqara", "Wireless Remote Switch H1 (Double Rocker)", "WXKG15LM"],
#     # 无线开关E1（贴墙式双键版）
#     'lumi.remote.acn004': ["Aqara", "Wireless Remote Switch E1 (Double Rocker)", "WXKG17LM"],
#     # 无线开关D1（贴墙式双键版）
#     'lumi.remote.b286acn02': ["Aqara", "Wireless Remote Switch D1 (Double Rocker)", "WXKG07LM"],
#     'params': [
#         {
#             "sensor": {
#                 MK_INIT_PARAMS: {
#                     MK_HASS_NAME: "action",
#                     "device_class": "",
#                     "state_class": "",
#                     "unit_of_measurement": ""
#                 },
#                 MK_RESOURCES: {"button": ("13.{}.85", "_attr_native_value")},
#                 MK_MAPPING_PARAMS: {"ch_count": 2},
#             }
#         }
#     ]
# }, 
{
    # 小米温湿度传感器
    'lumi.sensor_ht.v1': ["Xiaomi", "TH Sensor", "WSDCGQ01LM"],
    # 温湿度传感器
    'lumi.weather.v1': ["Aqara", "TH Sensor", "WSDCGQ11LM"],
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
},{
    # 高精度人体传感器
    'lumi.motion.agl04': ["Aqara", "Precision Motion Sensor", "RTCGQ13LM"],
    # 小米-人体移动传感器
    'lumi.sensor_motion.v1': ["Xiaomi", "Motion Sensor", "RTCGQ01LM"],
    'lumi.sensor_motion.v2': ["Xiaomi", "Motion Sensor", "RTCGQ01LM"],
    # 人体移动传感器
    'lumi.sensor_motion.aq2': ["Aqara", "Motion Sensor", "RTCGQ11LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "motion",
                    "device_class": DEVICE_CLASS_MOTION
                },
                MK_RESOURCES: {
                    "motion": ("3.1.85", "_attr_native_value"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }
    ]
},{
    # 人体存在
    'lumi.motion.ac01': ["Aqara", "Presence Sensor FP1", "RTCZCGQ11LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "motion",
                    "device_class": DEVICE_CLASS_MOTION
                },
                MK_RESOURCES: {
                    "motion": ("3.51.85", "_attr_native_value"),
                    "lqi": ("8.0.2007", "_attr_lqi")
                },
            }
        }
    ]
}, {
    # 门窗传感器
    'lumi.sensor_magnet': ["Xiaomi", "Door Sensor", "MCCGQ01LM"],
    'lumi.sensor_magnet.v2': ["Xiaomi", "Door Sensor", "MCCGQ01LM"],
    'lumi.sensor_magnet.aq2': ["Aqara", "Door Sensor", "MCCGQ11LM"],
    # 门窗传感器T1
    'lumi.magnet.agl02': ["Aqara", "Door Sensor T1", "MCCGQ12LM"],
    # 门窗传感器E1
    'lumi.magnet.acn001': ["Aqara", "Door Sensor E1", "MCCGQ14LM"],
    # 门窗传感器P1
    'lumi.magnet.ac01': ["Aqara", "Door Sensor P1", "MCCGQ13LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "contact",
                    "device_class": DEVICE_CLASS_DOOR
                },
                MK_RESOURCES: {
                    "status": ("3.1.85", "_attr_native_value"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }
    ]
}, {
    # 水浸传感器
    'lumi.sensor_wleak.aq1': ["Aqara", "Water Leak Sensor", "SJCGQ11LM"],
    'lumi.flood.agl02': ["Aqara", "Water Leak Sensor T1", "SJCGQ12LM"],
    'lumi.flood.acn001': ["Aqara", "Water Leak Sensor E1", "SJCGQ13LM"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "moisture",
                    "device_class": DEVICE_CLASS_MOISTURE
                },
                MK_RESOURCES: {
                    "moisture": ("3.1.85", "_attr_is_on"),
                    "lqi": ("8.0.2007", "_attr_lqi"),
                    "voltage": ("8.0.2008", "_attr_voltage")
                },
            }
        }
    ]
}, {
    # Xiaomi 烟雾报警器
    'lumi.sensor_smoke.v1': ["Xiaomi", "Smoke Sensor", "JTYJ-GD-01LM/BW"],
    'params': [
        {
            "binary_sensor": {
                MK_INIT_PARAMS: {
                    MK_HASS_NAME: "smoke",
                    "device_class": DEVICE_CLASS_SMOKE
                },
                MK_RESOURCES: {
                    "smoke": ("13.1.85", "_attr_is_on")
                },
            }
        }, 
    ]
}
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
