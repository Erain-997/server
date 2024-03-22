import time

from log.log import log_record
from start.api import api_login
import json
import requests

from start.telnet import put_down_key, telnet_ls, command_key, connect_telnet, execute_command
from start.tools import read_config


def api_get_voip(url, session_id):
    """
    :param url:
    :param session_id:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=voip"

    payload = {
        "api": "voip"
    }
    headers = {
        'Content-Type': 'application/json',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("GET", url + api_path, headers=headers, data=payload)
    print("api_get_voip", response.text)
    response_json = json.loads(response.text)
    return response_json


def api_set_voip(url, session_id, enable, display_name, user, userid, password, transport, proxy, h264):
    """
    :param url:
    :param session_id:
    :param enable:
    :param display_name:
    :param user:
    :param userid:
    :param password:
    :param transport:
    :param proxy:
    :param h264:
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=voip"

    payload = json.dumps({
        "enable": enable,
        "display_name": display_name,
        "user": user,
        "userid": userid,
        "password": password,
        "transport": transport,
        "proxy": proxy,
        "h264": h264
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", url + api_path, headers=headers, data=payload)
    print("api_set_voip", response.text)


def api_del_call_logs(url, session_id, index):
    """
    :param url:
    :param session_id:
    :param index:编辑、删除有该参数，参数说明：删除多个时 index分号分割如0;1;2, 为-1时删除全部
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=unlock_logs"

    payload = "index={}".format(index)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", "http://" + url + api_path, headers=headers, data=payload)
    print("api_del_call_logs", response.text)
    response_json = json.loads(response.text)
    return response_json


import xml.etree.ElementTree as ET
import re


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
# todo 这个特殊, 环境自己配好
if __name__ == '__main__':
    # call_url = "192.168.57.195"
    # called_url = "192.168.57.200"
    # # 环境准备
    # # 呼叫端配置
    # s1 = api_login(call_url)
    # voip1 = api_get_voip(call_url, s1)
    # api_set_voip(url=call_url, session_id=s1, enable="1", display_name=voip1["display_name"], h264="102",
    #              user="5998", userid="5998", password="Dnake@123", transport="0", proxy="sip:222.76.245.60:7788")
    # # 被呼叫端配置 todo 不同设备api不一样
    # s2 = api_login(called_url)
    # voip2 = api_get_voip(called_url, s2)
    # api_set_voip(url=called_url, session_id=s2, enable="1", display_name=voip1["display_name"], h264="102",
    #              user="5999", userid="5999", password="Dnake@123", transport="0", proxy="sip:222.76.245.60:7788")
    # 用户名密码
    tn = connect_telnet("192.168.57.195", 9900, "root", "1234321")
    if tn:
        # 测试次数
        for i in range(1, 11):
            # sip呼出,事先配置好
            shell_script = """
            #!/bin/sh
            /dnake/bin/dmsg /ui/v170/key data=*
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=C
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=C
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=#
            """
            # 执行命令
            execute_command(tn, shell_script)
            time.sleep(16)
            print("这是第{}次呼叫".format(i))
    else:
        print("发送指令失败")

    # 关闭 Telnet 连接
    tn.close()
