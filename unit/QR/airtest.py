# -*- encoding=utf8 -*-
__author__ = "dnake"

from airtest.core.api import *
import os
auto_setup(__file__)

cmd = "adb -s ZHSKUKMRVKAQRWTG shell input keyevent 26"
os.popen(cmd)

touch(Template(r"开app.png", record_pos=(-0.115, -0.301), resolution=(720, 1544)))


# cmd = "adb -s ZHSKUKMRVKAQRWTG shell settings put system screen_brightness 1"
# os.popen(cmd)
#
# for i in range(100):
#     touch(Template(r"点二维码.png", record_pos=(-0.324, -0.562), resolution=(720, 1544)))
#     time.sleep(1)

# poco("android.widget.FrameLayout").offspring("com.dnakesmart:id/toolbar_left_imgv").click()