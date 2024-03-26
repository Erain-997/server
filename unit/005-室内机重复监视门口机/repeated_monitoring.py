import sys
import threading

from airtest.core.api import *
from app.common import get_devices
# android项目的poco初始化
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from start.tools import read_config


def before_test():
    # todo 室内机设备端的设置页--Doors已搜索保存门口机
    devices = get_devices()
    print("devices: ", devices, "-----------")
    if len(devices) == 0:
        print("获取设备失败")
        return
    auto_setup(__file__, logdir=True, devices=devices[0])
    dev = connect_device("android:///" + devices[0])
    # 唤醒
    dev.wake()
    # 回主页
    dev.home()

    return dev


def set_ringing_time():
    pass


def test_repeated_monitoring(dev, duration):
    poco = AndroidUiautomationPoco(screenshot_each_action=False)

    touch(Template(r"监视.png", record_pos=(-0.098, 0.184), resolution=(1280, 800)))
    time.sleep(duration)
    print("return: ", "-----------")
    poco("android.widget.FrameLayout").offspring("com.dnake.talk:id/btn_close").click()

    dev.disconnect()
    sys.exit()


if __name__ == '__main__':
    # todo 裂开了, 从ide上跑
    try:
        # 获取测试数据
        data = read_config()
        durations = data.get('info', 'duration').split(',')
        times = data.get('info', 'times')
        print(durations, times)
        # device = before_test()
        device = connect_device("Android://127.0.0.1:5037/192.168.57.199:5555")
        device.wake()
        device.home()
        for i in durations:
            for j in times:
                # # 创建线程并启动
                # thread = threading.Thread(target=test_repeated_monitoring, args=(device, i))
                # thread.start()
                # # 等待子线程执行完成
                # thread.join()
                # sys.exit()
                test_repeated_monitoring(device, i)
    finally:
        sys.exit()
