# -*- encoding=utf8 -*-
__author__ = "dnake"

from app.common import connect_devices_ip, report
from airtest.core.api import *


def repeated_monitoring():
    model_name = "监视"
    ip = "192.168.57.199"
    report_name, poco = connect_devices_ip(model_name, ip)

    for i in range(2):
        touch(Template(r"监视.png", record_pos=(-0.098, 0.184), resolution=(1280, 800)))
        time.sleep(5)
        poco("android.widget.FrameLayout").offspring("com.dnake.talk:id/btn_close").click()

    report(os.path.dirname(os.path.realpath(__file__)), report_name)


if __name__ == '__main__':
    repeated_monitoring()
