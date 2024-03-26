# -*- encoding=utf8 -*-
# __author__ = "dnake"
import os
from airtest.core.api import *
from app.common import connect_devices, get_devices


def QR():
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

    # 用例内容
    time.sleep(10)
    for i in range(1000):
        touch(Template(r"点二维码.png", record_pos=(-0.324, -0.562), resolution=(720, 1544)))
        time.sleep(1)

    # poco("android.widget.FrameLayout").offspring("com.dnakesmart:id/toolbar_left_imgv").click()
    dev.disconnect()


if __name__ == '__main__':
    QR()
