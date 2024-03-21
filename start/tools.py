import socket


def get_local_ip():
    try:
        # 获取本地主机名
        host_name = socket.gethostname()
        # 获取本地 IP 地址
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except socket.error:
        return None


import configparser


def read_config():
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    # 读取 INI 文件
    config.read('cfg.ini')

    # 获取 'info' 节中的键值对
    section = 'info'
    url = config.get(section, 'url')
    times = config.getint(section, 'times')

    # 打印获取到的值
    print("URL:", url)
    print("Times:", times)
    return url, times
