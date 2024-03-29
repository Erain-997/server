import re
import time

from log.log import log_record
from start.api import api_login
import json
import requests

from start.telnet import connect_telnet, execute_command
from start.tools import read_config


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


def api_set_outdoor_device(url, session_id, mode, build, unit, index):
    """
    :param url:
    :param session_id:
    :param mode:
    :param build:
    :param unit:
    :param index:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=device"

    payload = "mode{}&build={}&unit={}&index={}".format(mode, build, unit, index)
    # print("payload: ", payload, "-----------")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    print("api_set_outdoor_device", response.text)
    response_json = json.loads(response.text)

    return response_json


def api_set_indoor_device(url, session_id, build, unit, room, index, sync):
    """
    :param url:
    :param session_id:
    :param build:
    :param unit:
    :param room:
    :param index:
    :param sync:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=device"

    payload = "build={}&unit={}&room{}&index={}&sync={}".format(build, unit, room, index, sync)
    # print("payload: ", payload, "-----------")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': "SessionID=" + session_id
    }
    print("http://" + url + api_path,22222222,payload)
    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    print("api_set_indoor_device", response.text)
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
    api_path = "/cgi-bin/webapi.cgi?api=call_logs"

    payload = "ringing={}&timeout={}".format(ringing, timeout)
    # print("payload: ", payload, "-----------")
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
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


def api_check_call_logs(data, times):
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
    number, duration = d.get('check', 'number'), d.getint('check', 'duration')
    for k, v in logs_data.items():
        if v["host"] == number and v["duration"] == duration:
            count += 1
        if v["duration"] != duration:
            if fail.get("响铃时间" + v["duration"] + "s"):
                fail["响铃时间" + v["duration"] + "s"] += 1
            else:
                fail["响铃时间" + v["duration"]] = 1
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
    # 呼叫设备
    call_url = data.get('call', 'url')
    # 被呼设备
    called_url = data.get('called', 'url')
    # 测试次数
    times = data.getint('info', 'times')
    build, unit, room = data.get('device', 'build'), data.get('device', 'unit'), data.get('device', 'room')

    # 设置室内机
    # 登录设备
    session = api_login(called_url)
    # 删除通话记录
    api_del_call_logs(called_url, session, "-1")
    # 设置响铃超时
    duration = data.get('check', 'duration')
    api_set_call_timeout(called_url, session, duration, "120")
    # 设置房号
    api_set_indoor_device(called_url, session, build, unit, room, "0", "578821")

    # 设置门口机
    # 登录设备
    session2 = api_login(call_url)
    api_set_outdoor_device(call_url, session2, "0", build, unit, 2)

    # 用户名密码
    tn = connect_telnet(call_url, 9900, "root", "1234321")
    if tn:
        # 测试次数
        for i in range(1, times):
            # 脚本内容
            shell_script = """
            #!/bin/sh
            /dnake/bin/dmsg /ui/v170/key data=*
            sleep 0.6
            /dnake/bin/dmsg /ui/v170/key data=2
            sleep 0.6
            /dnake/bin/dmsg /ui/v170/key data=8
            sleep 0.6
            /dnake/bin/dmsg /ui/v170/key data=1
            """

            # 执行命令
            execute_command(tn, shell_script)
            time.sleep(int(duration) + 3)
            # 有概率呼出失败
            logger.info("这是第{}次呼叫".format(i))
    else:
        logger.info("发送指令失败")

    # 等待振铃结束, 产生记录
    time.sleep(int(duration) + 3)
    # 登录被呼设备
    session = api_login(called_url)
    # 获取开锁记录
    log_path = api_get_call_logs(called_url, session)
    # 数据处理
    log = api_show_call_logs(called_url, session, log_path["file_name"])
    # 校验
    api_check_call_logs(str(log), times - 1)
    # 关闭 Telnet 连接
    tn.close()
