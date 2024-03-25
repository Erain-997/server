import os


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

    return devices

