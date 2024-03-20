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
