# -*- encoding=utf8 -*-
# __author__ = "dnake"
import os
from airtest.core.api import *
from app.common import connect_devices, get_devices
from log.log import log_record
from start.telnet import connect_telnet, execute_command


def QR():
    logger = log_record()
    device = get_devices()
    if len(device) == 0:
        print("-------沒鏈接設備-----------")
        return

    model_name = "二維碼開鎖"
    report_name, dev, poco = connect_devices(model_name, "ZHSKUKMRVKAQRWTG")
    # 杀
    dev.stop_app("com.dnakesmart")
    # 启动
    dev.start_app("com.dnakesmart")
    time.sleep(10)
    tn = connect_telnet("192.168.57.195", 9900, "root", "1234321")
    if tn:
        # 脚本内容
        shell_script = """
        #!/bin/sh
        /dnake/bin/dmsg /ui/v170/key data=*
        sleep 0.6
        /dnake/bin/dmsg /ui/v170/key data=*
        /dnake/bin/dmsg /ui/v170/key data=*
        sleep 0.6
        """
        # 执行命令
        execute_command(tn, shell_script)
    else:
        logger.info("发送指令失败")
    # 用例内容
    for i in range(10):
        touch(Template(r"点二维码.png", record_pos=(-0.324, -0.562), resolution=(720, 1544)))
        time.sleep(1)

    # poco("android.widget.FrameLayout").offspring("com.dnakesmart:id/toolbar_left_imgv").click()
    dev.disconnect()


if __name__ == '__main__':
    QR()
