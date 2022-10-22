# Aqara Bridge for Home Assistant

An integration of home-assistant which supports Aqara IoT Cloud.

[![version](https://img.shields.io/github/manifest-json/v/meishild/AqaraBridge?filename=custom_components%2Faqara_bridge%2Fmanifest.json)](https://github.com/meishild/AqaraBridge/releases/latest) [![stars](https://img.shields.io/github/stars/meishild/AqaraBridge)](https://github.com/meishild/AqaraBridge/stargazers) [![issues](https://img.shields.io/github/issues/meishild/AqaraBridge)](https://github.com/meishild/AqaraBridge/issues) [![hacs](https://img.shields.io/badge/HACS-Default-orange.svg)](https://hacs.xyz)


## 需要开发者账号支持

申请AqaraIOT开发者：[Aqara IoT Cloud](https://developer.aqara.com/register).

* 提示：此集成不支持通过UI配置。大概率是因为rocketmq的链接库不存在，暂时只自动集成了x86和arm64其他要自己想办法。
## 版本修订

遗留问题：
* 当前出会出现存储问题，需要修复。

V2.0
* 修改flow，将多个网关合并到账号，拆分开发者认证信息允许自行配置自己的开发者AK等。
* 修复大部分组件获取状态异常，以及历史状态修改。
* 感谢银狼新增：支持无线旋钮H1，H1 12头磁吸格栅灯，无线按钮（升级版）。同时墙壁开关拆分为两部分，其中零火的加入了电量监测，led驱动模块加了电力监测。

V1.1
* 修复了大部分组件的问题，增加了无线按键。当前的按键都同时事件订阅刷新时间整体速度还不错，不是轮训机制了。
* 增加房间位置获取。
* 增加按键类开关对应按键名称获取。
* 增加arm64的rocketmq动态链接库，除了X86和arm64其他暂时没处理。
* 增加各类的历史数据获取刷新了最后的trigger_time或者last_update_time。
* 增加button类型，将无线开关从传感器上拆分。
* 配置了大部分常见的网关、无线开关、单火/零火开关、温湿度传感器、智能插座、人体传感器等。
* 增加了部分错误提示，至少不会在配置没任何错误了。

V1.0

还有我只支持了大部分我有的设备和类似的组建，如果发现有不支持的懂python的修改：
https://github.com/meishild/Aqar ... ore/aiot_mapping.py

