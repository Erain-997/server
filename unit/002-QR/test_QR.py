# -*- encoding=utf8 -*-
# __author__ = "dnake"
import os
from airtest.core.api import *


def test_QR():
    # auto_setup(__file__)
    # connect an android phone with adb
    dev = connect_device("android:///ZHSKUKMRVKAQRWTG")
    # 唤醒
    dev.wake()
    # 杀
    dev.stop_app("com.dnakesmart")
    # # set_current(0)
    # dev.shell("adb --version")
    # 启动
    dev.start_app("com.dnakesmart")
    time.sleep(10)
    for i in range(100):
        touch(Template(r"点二维码.png", record_pos=(-0.324, -0.562), resolution=(720, 1544)))
        time.sleep(1)

    # poco("android.widget.FrameLayout").offspring("com.dnakesmart:id/toolbar_left_imgv").click()
    dev.disconnect()


if __name__ == '__main__':
    test_QR()
