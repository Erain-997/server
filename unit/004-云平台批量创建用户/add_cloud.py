from log.log import log_record
from start.api_cloud import api_cloud_login

import json
import requests


def api_cloud_creat_user(token, room):
    api_path = "https://test.api.cloud.ishanghome.com/admin-api/business/resident/create"
    payload = json.dumps({
        'bindDeviceIds': ['1768909428213202945'],
        'buildingId': '1719287244324462592',
        'buildingName': '10',
        'country': 'Thailand',
        'countryId': '222',
        'email': 'test' + str(room) + '@qq.com',
        'enableApp': 1,
        'hasIndoorMonitor': 0,
        'language': 'English',
        'languageId': '5',
        'mobile': '2123' + str(room),
        'name': 'First' + str(room),
        'roomId': '',
        'roomName': room,
        'surname': 'Last' + str(room),
        'unitId': '1745646339714617344',
        'unitName': '20',
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", api_path, headers=headers, data=payload)
    response_json = json.loads(response.text)
    logger.info("云平台创建用户:{},{}".format(room,response_json))
    return response_json


def api_open_country_list(token):
    api_path = "https://test.api.cloud.ishanghome.com/admin-api/business/country/openCountryList"
    payload = json.dumps({
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", api_path, headers=headers, data=payload)
    response_json = json.loads(response.text)
    print("api_open_country_list: ", response_json, "-----------")
    return response_json

logger = log_record()
if __name__ == '__main__':
    token = api_cloud_login("tai1234@qq.com", "Ye990605")
    # api_open_country_list(token, 5001)
    for i in range(5002, 5201):
        api_cloud_creat_user(token, i)
