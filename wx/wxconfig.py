#!/usr/bin/python
# coding=utf-8

__author__ = 'testerzhang'

WX_LOG = "logs/wx.log"

DEVICE_NAME = 'xiaomi'
DEVICE_PORT = '4723'

# 安卓版本
ANDROID_VERSION = "11"
# APP Package 名字
APP_PACKAGE_NAME = "com.tencent.mm"
# APP Activity 名字
APP_ACTIVITY_NAME = "com.tencent.mm.ui.LauncherUI"

DESIRED_CAPS = {
    "platformName": "Android",
    "platformVersion": ANDROID_VERSION,
    "deviceName": DEVICE_NAME,
    "appPackage": APP_PACKAGE_NAME,
    "appActivity": APP_ACTIVITY_NAME,

    # 再次启动不需要再次安装
    "noReset": True,
    # unicode键盘 我们可以输入中文
    "unicodeKeyboard": True,
    # 操作之后还原回原先的输入法
    "resetKeyboard": True
}

# 开启状态：是否只进行滑动屏幕测试.第一次可以设置True，这样可以获取联系人名称
SLIDE_TEST = True
#SLIDE_TEST = False

# 下滑次数
SLIDE_TIMES = 100

# 聊天窗口的xpath路径，通过定位元素获取录入到这里。
CHAT_XPATH = "com.tencent.mm:id/fzg"

SKIP_CONTACT_LISTS = [
    # 通知
    "订阅号消息",
]

