import time
from start.api import api_login
import json
import requests

from start.telnet import put_down_key, telnet_ls, command_key, connect_telnet, execute_command

if __name__ == '__main__':
    # 用户名密码
    tn = connect_telnet("192.168.57.195", 9900, "root", "1234321")
    if tn:
        # 测试次数
        for i in range(1, 11):
            # 脚本内容
            shell_script = """
            #!/bin/sh
            /dnake/bin/dmsg /ui/v170/key data=*
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=2
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=8
            sleep 0.5
            /dnake/bin/dmsg /ui/v170/key data=0
            """

            # 执行命令
            execute_command(tn, shell_script)
            time.sleep(16)
            print("这是第{}次呼叫".format(i))
    else:
        print("发送指令失败")

    # 关闭 Telnet 连接
    tn.close()
