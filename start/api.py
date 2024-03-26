import json
import requests


def api_login(url):
    """
    :param url: 192.168.57.200
    :return:
    """
    api_path = "/cgi-bin/webapi.cgi?api=login&username=admin&password=e10adc3949ba59abbe56e057f20f883e"
    payload = {}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }
    # md5_password = hashlib.md5(password.encode()).hexdigest()  # 将密码转换为 MD5
    response = requests.request("GET", "http://" + url + api_path, headers=headers, data=payload)
    if len(response.cookies) > 0:
        print("新服务器SessionId:", response.cookies["SessionID"].strip())
        return response.cookies["SessionID"].strip()
    # 解析 JSON 数据
    print(response.text, 11)
    response_json = json.loads(response.text)
    print("旧服务器SessionId:", response_json['data']['SessionID'].strip())
    return response_json['data']['SessionID'].strip()


def api_set_current_device_configuration(url, session_id, panel_mode, building: int, unit: int, floor: int,
                                         apartment: int, device_number: int,
                                         no_unit: bool):
    """
    :param url:
    :param session_id:
    :param panel_mode:Allowed values:Unit, Gate Station, Villa
    :param building: >= 0,<= 999
    :param unit: >= 0,<= 99
    :param floor: >= 0,<= 98
    :param apartment: >= 0,<= 99
    :param device_number: >= 0,<= 9
    :param no_unit:
    :return:
    """
    api_path = "/api/v1/device/settings"

    payload = json.dumps({
        "panel_mode": panel_mode,
        "building": building,
        "unit": unit,
        "floor": floor,
        "apartment": apartment,
        "device_number": device_number,
        "no_unit": no_unit
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': "SessionID=" + session_id
    }

    response = requests.request("POST", url + api_path, headers=headers, data=payload)
    print(response.text)
