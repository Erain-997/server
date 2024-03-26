# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
#
# poco = AndroidUiautomationPoco()
# poco.device.wake()


from airtest.core.api import connect_device

# # 远程设备连接信息
# remote_device = {"device": "Android://192.168.57.199:5555/8b85c25899675881"}
#
# # 连接远程设备
# connect_device(remote_device)

dev = connect_device("Android://127.0.0.1:5037/192.168.57.199:5555")
dev.wake()
