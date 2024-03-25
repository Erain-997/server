import json
import re
import time
import xml.etree.ElementTree as ET

import requests

from start.api import api_login
from start.telnet import connect_telnet, execute_command
from start.tools import read_config

from log.log import log_record

"""
"0":"卡","1":"密码","2":"对讲","3":"出门按钮","_4":"人脸","5":"APP","6":"HTTP",

  "unlockLogs.status.option_0": "失败",
    "unlockLogs.status.option_1": "成功",
"""


def api_del_unlock_password(url, session_id, index):
    """
    :param url:
    :param session_id:
    :param index:编辑、删除有该参数，参数说明：删除多个时 index分号分割如0;1;2, 为-1时删除全部
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=unlock_passwd"

    payload = "action=0&index={}".format(index)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    # print("api_del_unlock_password", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_del_unlock_logs(url, session_id, index):
    """
    :param url:
    :param session_id:
    :param index:编辑、删除有该参数，参数说明：删除多个时 index分号分割如0;1;2, 为-1时删除全部
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=unlock_logs"

    payload = "action=0&index={}".format(index)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    # print("api_del_unlock_logs", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_set_unlock_password(url, session_id, action, password, relays):
    """
    :param url:
    :param session_id:
    :param action:范围：0-2，参数说明：0: 删除, 1: 添加 2：编辑
    :param password:
    :param relays:继电器选择，如: 0,2（选中第1、3路继电器）
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=unlock_passwd"

    payload = "action={}&password={}&relays={}".format(str(action), password, relays)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    # print("api_set_unlock_password", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_get_unlock_password(url, session_id):
    """
    :param url:
    :param session_id:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=unlock_passwd"

    payload = json.dumps({
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("GET", "http://" + url + api_path, headers=headers, data=payload)
    # print("api_get_unlock_password", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_get_unlock_logs(url, session_id):
    """
    :param url:
    :param session_id:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=unlock_logs"

    payload = json.dumps({
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("GET", "http://" + url + api_path, headers=headers, data=payload)
    # print("api_get_unlock_logs", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_show_unlock_logs(url, session_id, log_path):
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
    # print("api_show_unlock_logs", response.text)
    # response_json = json.loads(response.text)
    return response.text


def api_check_unlock_logs(data, times):
    # 解析 XML 字符串
    root = ET.fromstring(data)
    # 获取 max 字段
    max_value = root.find('max').text
    logger.info('总的记录条数:{}'.format(max_value))
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
    number, status = d.get('check', 'number'), d.getint('check', 'status')
    for k, v in logs_data.items():
        if v["number"] == number and v["status"] == str(status):
            count += 1
        if v["status"] != "0":
            fail["number"] += 1
    if count == times:
        logger.info("测试成功")
        logger.info("开锁成功条数:{},脚本执行次数:{}".format(count, times))
    else:
        logger.info("开锁成功条数:{},脚本执行次数:{}".format(count, times))
        logger.info("失败次数:{},号码以及对应次数:{}".format(len(fail), fail))


logger = log_record()
if __name__ == '__main__':
    # 获取测试数据
    data = read_config()
    url, times = data.get('info', 'url'), data.getint('info', 'times')
    # 登录设备
    session = api_login(url)
    # 删除开锁密码
    api_del_unlock_password(url, session, "-1")
    # 删除开锁记录
    api_del_unlock_logs(url, session, "-1")
    # 新增门锁
    api_set_unlock_password(url, session, 1, "9999", "0")
    # 查看密码
    api_get_unlock_password(url, session)
    # 用户名密码
    tn = connect_telnet(url, 9900, "root", "1234321")

    if tn:
        # 测试次数
        for i in range(1, times + 1):
            # 开锁
            shell_script = """
            #!/bin/sh
            /dnake/bin/dmsg /ui/v170/key data=*
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=#
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=9
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=9
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=9
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=9
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=#
            """
            # 执行命令
            execute_command(tn, shell_script)
            logger.info("这是第{}次开锁".format(i))
            time.sleep(8)
    else:
        logger.info("发送指令失败")

    # 登录设备
    session = api_login(url)
    # 获取开锁记录
    log_path = api_get_unlock_logs(url, session)
    # 数据处理
    log = api_show_unlock_logs(url, session, log_path["file_name"])
    # 校验
    api_check_unlock_logs(str(log), times)

    # 关闭 Telnet 连接
    tn.close()
