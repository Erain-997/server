import json
import requests


def api_cloud_login(username, password):
    """
    :param url: 192.168.57.200
    :return:
    """
    api_path = "https://test.api.cloud.ishanghome.com/admin-api/system/auth/login"
    payload = json.dumps({
        # "captchaVerification": "PfcH6mgr8tpXuMWFjvW6YVaqrswIuwmWI5dsVZSg7sGpWtDCUbHuDEXl3cFB1+VvCC/rAkSwK8Fad52FSuncVg==",
        # "socialState": "9b2ffbc1-7425-4155-9894-9d5c08541d62",
        # "socialCode": 1024,
        # "socialType": 10,
        "username": username,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }
    # md5_password = hashlib.md5(password.encode()).hexdigest()  # 将密码转换为 MD5
    response = requests.request("POST", api_path, headers=headers, data=payload)
    # 解析 JSON 数据
    print(response.text, 11)
    response_json = json.loads(response.text)
    print("云服务器accessToken:", response_json['data']['accessToken'].strip())
    return response_json['data']['accessToken'].strip()
