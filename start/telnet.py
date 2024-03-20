import telnetlib
import time


def connect_telnet_finish(output):
    pass


def connect_telnet(url, port, username, password):
    try:
        # 创建 Telnet 连接对象
        tn = telnetlib.Telnet(url, port)

        print("Telnet连接启动: ", url, port, username, password)
        time.sleep(0.5)
        # 读取登录提示信息
        tn.read_until(b"login: ")
        # 输入用户名
        tn.write(username.encode('ascii') + b"\n")
        # 读取密码提示信息
        tn.read_until(b"Password: ")
        # 输入密码
        tn.write(password.encode('ascii') + b"\n")
        # if tn.read_until(b"root@v904:/ #"):
        #     print("登录成功")
        return tn
    except Exception as e:
        print("Telnet连接出错:", str(e))
        return None


def execute_command(tn, command):
    try:
        # 登录后执行命令
        tn.write(command.encode('ascii') + b"\n")
    except Exception as e:
        print("命令执行出错:", str(e))


def execute_command_back(tn, command):
    try:
        # 登录后执行命令
        tn.write(command.encode('ascii') + b"\n")
        time.sleep(2)
        # 读取命令输出
        output = ""
        while True:
            check = output
            # 逐行读取输出
            line = tn.read_until(b"\n", timeout=3).decode('ascii')
            time.sleep(0.2)
            # print(datetime.datetime.now(), "11: ", line)
            if line.endswith(":/ # "):
                print(command + "命令执行完毕")
                # 判断行是否以换行符结尾
                break
            output += line
            # 容错
            if check == output:
                print(command + "无输出结束")
                break

        # 输出命令输出结果
        print("output: ", output)
    except Exception as e:
        print("命令执行出错:", str(e))


def command_key(arg):
    return "/dnake/bin/dmsg /ui/v170/key data=" + arg


def put_down_key(url, arg: list):
    tn = connect_telnet(url, 9900, "root", "1234321")
    if tn:
        # 执行命令
        for i in arg:
            time.sleep(0.5)
            send_key = command_key(i)
            print(send_key)
            time.sleep(1)
            execute_command(tn, send_key)
            time.sleep(0.5)
        # 关闭 Telnet 连接
        tn.close()
    else:
        print("发送指令失败")


# todo demo test
def telnet_ls(url, port, username, password):
    tn = connect_telnet(url, port, username, password)
    if tn:
        # 执行命令
        execute_command_back(tn, "ls")
        # 关闭 Telnet 连接
        tn.close()
    else:
        print("Telnet连接失败")
