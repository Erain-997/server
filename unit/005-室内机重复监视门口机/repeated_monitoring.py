# -*- encoding=utf8 -*-
__author__ = "dnake"

import json
import re

import requests

from app.common import connect_devices_ip, report
from airtest.core.api import *

from log.log import log_record
from start.api import api_login
from start.tools import read_config

def api_enable_call_logs(url, session_id, enable):
    """
    :param url:
    :param session_id:
    :param index:编辑、删除有该参数，参数说明：删除多个时 index分号分割如0;1;2, 为-1时删除全部
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=call_logs"

    payload = "enable={}".format(enable)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    print("api_enable_call_logs", response.text)
    response_json = json.loads(response.text)
    return response_json

def api_del_call_logs(url, session_id, index):
    """
    :param url:
    :param session_id:
    :param index:编辑、删除有该参数，参数说明：删除多个时 index分号分割如0;1;2, 为-1时删除全部
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=call_logs"

    payload = "index={}".format(index)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    print("api_del_call_logs", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_set_call_timeout(url, session_id, ringing, timeout):
    """
    :param url:
    :param session_id:
    :param ringing:响铃时间
    :param timeout:通话时间
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=call"

    payload = "dial_mode=0ringing={}&timeout={}".format(ringing, timeout)
    # print("payload: ", payload, "-----------")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    print("api_set_call_timeout", response.text)
    response_json = json.loads(response.text)

    return response_json


def api_get_call_logs(url, session_id):
    """
    :param url:
    :param session_id:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=call_logs"

    payload = json.dumps({
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("GET", "http://" + url + api_path, headers=headers, data=payload)
    # print("api_get_call_logs", response.text)
    response_json = json.loads(response.text)

    return response_json


def api_show_call_logs(url, session_id, log_path):
    """
    :param url:
    :param session_id:
    :return:
    """

    payload = json.dumps({
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("GET", "http://" + url + log_path, headers=headers, data=payload)

    return response.text


import xml.etree.ElementTree as ET


def api_check_call_logs(data, times, check_duration):
    # 解析 XML 字符串
    root = ET.fromstring(data)
    # 获取 max 字段
    max_value = root.find('max').text
    print('总的记录条数:', max_value)
    # 数据处理, 处理出每一条记录
    logs_data = {}
    # 查找并分组元素
    pattern = re.compile(r'^d\d+$')  # 匹配以 "d" 开头并后跟数字的字符串
    for element in root.iter():
        if pattern.match(element.tag):
            # grouped_elements.append(element)
            d = {}
            for j in element:
                d[j.tag] = j.text
            logs_data[element.tag] = d

    print("logs_data", len(logs_data))
    print("数据内容", logs_data)

    # 以下是数据校验
    count = 0
    fail = {}
    # 获取测试数据
    d = read_config()
    number = d.get('check', 'number')
    for k, v in logs_data.items():
        if v["number"] == number and v["timeout"] == check_duration:
            count += 1
        if v["timeout"] != check_duration:
            if fail.get("响铃时间" + v["timeout"] + "s"):
                fail["响铃时间" + v["timeout"] + "s"] += 1
            else:
                fail["响铃时间" + v["timeout"]] = 1
    if count == times:
        logger.info("测试成功")
        logger.info("被呼叫成功条数:{},脚本执行次数:{}".format(count, times))
    else:
        logger.info("被呼叫成功条数:{},脚本执行次数:{}".format(count, times))
        logger.info("失败次数:{},号码以及对应次数:{}".format(len(fail), fail))


logger = log_record()
if __name__ == '__main__':
    # 获取测试数据
    data = read_config()
    # 用例名称
    case_name = data.get('info', 'case_name')
    # 测试次数
    times = data.getint('info', 'times')
    # 呼叫设备
    call_url = data.get('call', 'url')
    # 被呼设备
    called_url = data.get('called', 'url')
    # 响铃超时时间
    durations = data.get('check', 'duration').split(',')

    # 连接呼叫设备
    report_name, poco = connect_devices_ip(case_name, call_url)
    for duration in durations:
        # 登录被呼设备
        session = api_login(called_url)
        # 开启通话记录
        api_enable_call_logs(called_url, session, "1")
        # 删除通话记录
        # api_del_call_logs(called_url, session, "-1")
        # 设置响铃超时
        print("11111",duration)
        api_set_call_timeout(called_url, session, "10", duration)

        # 执行用例
        for i in range(times):
            touch(Template(r"监视.png", record_pos=(-0.098, 0.184), resolution=(1280, 800)))
            time.sleep(int(duration) + 2)
            poco("android.widget.FrameLayout").offspring("com.dnake.talk:id/btn_close").click()
            time.sleep(1)

        # 等待振铃结束, 产生记录
        time.sleep(int(duration) + 3)
        # 登录被呼设备
        session = api_login(called_url)
        # 获取被呼记录
        log_path = api_get_call_logs(called_url, session)
        # 数据处理
        log = api_show_call_logs(called_url, session, log_path["file_name"])
        # 校验
        api_check_call_logs(str(log), times - 1, int(duration))

    report(os.path.dirname(os.path.realpath(__file__)), report_name)
