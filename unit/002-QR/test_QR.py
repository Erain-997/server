# -*- encoding=utf8 -*-
# __author__ = "dnake"
import os
from airtest.core.api import *


def test_QR():
    auto_setup(__file__)
    # connect an android phone with adb
    dev = connect_device("Android:///ZHSKUKMRVKAQRWTG")
    dev.wake()
    dev.clear_app("com.dnakesmart")
    # set_current(0)
    # dev.shell("adb --version")
    # dev.shell("adb -s ZHSKUKMRVKAQRWTG shell input keyevent 26")
    # 连接设备
    # device = connect_device("android://ZHSKUKMRVKAQRWTG")

    dev.start_app("com.dnakesmart")
    # touch(Template(r"开app.png", record_pos=(-0.115, -0.301), resolution=(720, 1544)))

    dev.disconnect()
    print("我结束了")

    # for i in range(100):
    #     touch(Template(r"点二维码.png", record_pos=(-0.324, -0.562), resolution=(720, 1544)))
    #     time.sleep(1)

    # poco("android.widget.FrameLayout").offspring("com.dnakesmart:id/toolbar_left_imgv").click()


if __name__ == '__main__':
    test_QR()