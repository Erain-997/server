# 命令
adb shell pm list packages
```shell script
# 安装启动com.dnakesmart
adb -s ZHSKUKMRVKAQRWTG shell am start -n com.dnakesmart/.MainActivity
adb -s ZHSKUKMRVKAQRWTG shell am start com.dnakesmart
adb -s ZHSKUKMRVKAQRWTG shell am start com.dnakesmart/com.dnake.main.ui.SplashActivity
# 查看正在运行的包体
adb -s ZHSKUKMRVKAQRWTG shell dumpsys activity | findstr "mFocusedActivity"
# 查看包体
adb -s ZHSKUKMRVKAQRWTG shell pm list packages
# 设置亮度
adb -s ZHSKUKMRVKAQRWTG shell settings put system screen_brightness 50
# 模拟按下设备的电源按钮，从而点亮屏幕
adb -s ZHSKUKMRVKAQRWTG shell input keyevent 26
adb -s ZHSKUKMRVKAQRWTG shell am start com.smewise.camera2

```