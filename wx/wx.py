#!/usr/bin/python
# coding=utf-8
# 公众号:testerzhang
__author__ = 'testerzhang'

import time
import traceback

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import parse
from loguru import logger

import wxconfig as config

logger.add(config.WX_LOG)


def wait_time_bar(wait_sec):
    logger.debug(f"等待{wait_sec}秒")
    wait_value = 10 * wait_sec

    for i in tqdm(range(wait_value)):
        time.sleep(0.1)

    # logger.debug("")


class WX(object):
    def __init__(self):
        device_port = config.DEVICE_PORT

        desired_caps = config.DESIRED_CAPS

        self.skip_list = config.SKIP_CONTACT_LISTS

        url = "http://localhost:{}/wd/hub".format(device_port)

        self.driver = webdriver.Remote(url, desired_caps)

        logger.debug("1.打开微信")
        wait_time_bar(4)

    # 关闭
    def close(self):
        wait_time_bar(5)
        logger.debug("6.关闭app")
        self.driver.quit()

    # 判断某些联系人是不是直接跳过
    def continue_contact(self, contact):
        is_continue = True
        for skip in self.skip_list:
            if skip in contact:
                logger.warning(f"联系人=[{contact}]暂时不做")
                is_continue = False
                break

        return is_continue

    def clean_chat_lists(self):
        # 备注下，识别不了企业群
        chat_xpath = config.CHAT_XPATH
        list_view_rows = self.driver.find_elements_by_id(chat_xpath)
        logger.debug(f"列表长度={len(list_view_rows)}")

        if len(list_view_rows) < 1:
            logger.warning(f"列表长度为空，退出")
            return

        for i, list_view_row in enumerate(list_view_rows, 1):
            logger.debug(f"处理第{i}个联系人")
            # 定位聊天记录列表，选第一个长按
            el = list_view_row
            try:
                el_name = el.text
                logger.debug(f"联系人姓名={el_name}")
            except NoSuchElementException:
                logger.warning(f"获取姓名异常，跳过")
                continue

            if not self.continue_contact(el_name):
                logger.warning(f"跳过")
                continue

            # 如果是开启测试，则只记录联系人名称。
            if config.SLIDE_TEST:
                continue

            # 长按
            TouchAction(self.driver).long_press(el).perform()
            wait_time_bar(1)

            try:
                # 定位选项框'不显示该聊天'
                self.driver.find_element_by_xpath("//*[@text='不显示该聊天']").click()
                wait_time_bar(2)
            except NoSuchElementException:
                logger.warning(f"[不显示该聊天]菜单出不来，退出")
                break
            except:
                logger.error(f"[不显示该聊天]菜单点击异常")

            try:
                # 定位选项框'我知道了'提醒框，非必须
                self.driver.find_element_by_xpath("//*[@text='我知道了']").click()
                wait_time_bar(2)
            except NoSuchElementException:
                pass
            except:
                logger.error(f"提醒框【我知道了】点击异常")

            # 定位选项框'不显示'
            try:
                self.driver.find_element_by_xpath("//*[@text='不显示']").click()
                wait_time_bar(2)
            except NoSuchElementException:
                logger.warning(f"[不显示]确认框找不到，退出")
                break
            except:
                logger.error(f"[不显示]确认框点击异常")
                break

    #  gzh:testerzhang 进入微信列表页面
    def do(self):
        # 下滑次数
        slide_times = config.SLIDE_TIMES
        begin_times = 1

        # 获取屏幕的高、宽
        middle_pos = self.driver.get_window_size()
        logger.debug(f"middle_pos={middle_pos}")

        # 获取屏幕的高
        x = self.driver.get_window_size()['width']
        # 获取屏幕宽
        y = self.driver.get_window_size()['height']

        self.clean_chat_lists()

        while begin_times <= slide_times:
            logger.debug(f"第{begin_times}次滑动")

            start_x = 1 / 2 * x
            start_y = 1 / 2 * y
            distance = 600

            self.driver.swipe(start_x, start_y, start_x, start_y - distance)

            begin_times = begin_times + 1

            self.clean_chat_lists()
            wait_time_bar(1)

        #


def main():
    wx = WX()
    wx.do()
    wx.close()
    exit("退出")


if __name__ == '__main__':
    main()

