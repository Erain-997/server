import time
from start.api import api_login
import json
import requests

from start.telnet import put_down_key, telnet_ls, command_key, connect_telnet, execute_command


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


if __name__ == '__main__':
    call_url = "192.168.57.195"
    called_url = "192.168.57.200"
    # 环境准备
    # 呼叫端配置
    s1 = api_login(call_url)
    voip1 = api_get_voip(call_url, s1)
    api_set_voip(url=call_url, session_id=s1, enable="1", display_name=voip1["display_name"], h264="102",
                 user="5998", userid="5998", password="Dnake@123", transport="0", proxy="sip:222.76.245.60:7788")
    # 被呼叫端配置 todo 不同设备api不一样
    s2 = api_login(called_url)
    voip2 = api_get_voip(called_url, s2)
    api_set_voip(url=called_url, session_id=s2, enable="1", display_name=voip1["display_name"], h264="102",
                 user="5999", userid="5999", password="Dnake@123", transport="0", proxy="sip:222.76.245.60:7788")
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
