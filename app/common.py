import os

from airtest.report.report import simple_report


def get_devices():
    # 执行 adb 命令获取设备列表
    command = 'adb devices'
    output = os.popen(command).read()

    # 解析输出获取设备列表
    devices = []
    lines = output.strip().split('\n')
    for line in lines[1:]:
        if '\t' in line:
            device_id, device_status = line.split('\t')
            if device_status == 'device':
                devices.append(device_id)
    time.sleep(2)
    return devices


def connect_devices(name, device):
    import datetime
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not cli_setup():
        auto_setup(__file__, compress=False, logdir="./report_" + name + f"_{current_time}")

    dev = connect_device("android:///" + device)
    poco = AndroidUiautomationPoco()
    wake()
    home()
    return name + f"_{current_time}", dev, poco


from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


def connect_devices_ip(name, ip):
    import datetime
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not cli_setup():
        auto_setup(__file__, compress=False, logdir="./report_" + name + f"_{current_time}",
                   devices=["Android://127.0.0.1:5037/" + ip + ":5555", ])

    poco = AndroidUiautomationPoco()
    wake()
    home()
    return name + f"_{current_time}", poco


from airtest.core.settings import Settings


def report(path, report_name):
    # 修改 Airtest 框架的默认配置, 不要小截圖
    Settings.SNAPSHOT_QUALITY = False
    res_path = path + "\\report_" + report_name
    # generate html report
    simple_report(__file__, logpath=os.path.abspath(res_path), output=False)
    # 文件夹路径
    print("文件夹路径:", res_path)
    os.popen(f'explorer "{res_path}"')
