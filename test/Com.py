import serial
from enum import Enum
import time

class Mode(Enum):
    x_distance = 1
    y_distance = 2
    rotate = 3

    x_dis_mm = 5
    y_dis_mm = 6
    grub_1 = 7  # 从原料区抓取物料块
    grub_2 = 8  # 从地面抓取物料块
    down_1 = 9  # 将物料块放到地面上
    down_2 = 10 # 精加工区，将物料块放到另一个物料块上
    adjust_height = 11 # 调整升降台到合适的位置    1.读取二维码  2.识别原料区  3.识别圆环   4.识别物料块圆心 
    adjust_height_manual = 12
    mix_mode = 13 # 混动模式，一边底盘移动，一边移动升降台

class HeightMode(Enum):
    qrPos = 1
    rawArea = 2
    circleArea = 3
    stackArea = 4
    # 二维码任务代码与颜色的对应

# 定义信号值
header = 0xFF
mode = 0x00
x_dis = 0x00
y_dis = 0x00
angel = 0x00
tail = 0xFE

send_byte = bytearray([header, mode, x_dis, y_dis, angel, tail])

color_list = [0, "red", "green", "blue"]

# 粗加工颜色顺序
color_list_in_rough_area = ['green', 'red', 'blue']

# 精加工颜色顺序
color_list_in_fine_area = ['green', 'red', 'blue']

# 色块之间的距离
dis_between_every_circle = 0.15

pi = 3.14159

ser = serial.Serial(port='/dev/pts/6',
                    baudrate=115200,
                    bytesize=8,
                    parity=serial.PARITY_NONE,
                    stopbits=1)  # open serial port

def wait_for_start():
    while True:
        
        data = ser.readline().decode().strip()
        if data:
            if data == "start":
                print("Start")
                
                break

# 接收数据并执行任务函数
def receive_and_execute_tasks():
    try:
        while True:
            data = ser.readline().decode().strip()  # 读取并解码串口数据
            if data:
                # 根据接收到的数据执行不同的任务
                if data == "correct_path":
                    print("well done")
                else:
                    # 处理未知数据
                    handle_unknown_data(data)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()  # 关闭串口连接


# 将整数值转换为有符号8位整数（int8_t）的方法
def convert_to_int8(value):
    value = int(value)
    if value > 127:
        return -(256 - value)
    return value

# 生成串口数据、发送数据并等待回传结果
def send_serial_msg(serial,mode, x_dis=None, y_dis=None, angel=None):

    if mode == Mode.x_distance:
        assert x_dis != None, print("未指定x方向移动距离")
        send_byte[1] = mode.value
        send_byte[2] = convert_to_int8(x_dis)

    elif mode == Mode.y_distance:
        assert y_dis != None, print("未指定y方向移动距离")
        send_byte[1] = mode.value
        send_byte[3] = convert_to_int8(y_dis)

    elif mode == Mode.rotate:
        assert angel != None, print("未设置角度")
        send_byte[1] = mode.value
        send_byte[4] = convert_to_int8(angel)


    elif mode == Mode.x_dis_mm:
        assert x_dis != None, print("未指定x方向移动距离，单位:毫米")
        send_byte[1] = mode.value
        send_byte[2] = convert_to_int8(x_dis)

    elif mode == Mode.y_dis_mm:
        assert y_dis != None, print("未指定x方向移动距离，单位:毫米")
        send_byte[1] = mode.value
        send_byte[3] = convert_to_int8(y_dis)

    # 从原料区抓取物料块
    elif mode == Mode.grub_1:
        send_byte[1] = mode.value

    # 从地面抓取物料块
    elif mode == Mode.grub_2:
        send_byte[1] = mode.value

    # 将物料块放到地面上
    elif mode == Mode.down_1:
        send_byte[1] = mode.value

    # 在精加工区，将物料块放到另一个物料块
    elif mode == Mode.down_2:
        send_byte[1] = mode.value
    
    # 调整升降台的位置
    elif mode == Mode.adjust_height:
        send_byte[1] = mode.value
        send_byte[2] = x_dis.value

    elif mode == Mode.adjust_height_manual:
        send_byte[1] = mode.value
        send_byte[2] = x_dis.value
        raise NotImplementedError('这个模式还没有实现')
    
    elif mode == Mode.mix_mode:
        send_byte[1] = mode.value
        send_byte[2] = y_dis.value
        send_byte[3] = convert_to_int8(x_dis)

    else:
        raise ValueError("下位机模式选择错误，现有的模式有", [mode.name for mode in Mode])

    serial.write(send_byte)
    print(send_byte)
    wait_for_movement_done(ser)
    time.sleep(0.05)

def set_distance(serial, x=0, y=0):
    x = 1e-9 if x == 0 else x
    y = 1e-9 if y == 0 else y
    #后续有参数微调需要 max_one_time_dis 
    max_one_time_dis = 1.25
    if abs(x) > max_one_time_dis or abs(y) > max_one_time_dis:
        Warning("单次距离设置最远为{0}，需多次调用".format(max_one_time_dis))
    #计算移动次数
    times_x, times_y = int(abs(x) / max_one_time_dis), int(
        abs(y) // max_one_time_dis
    )
    #计算剩余的移动距离
    rest_x, rest_y = (
        abs(x) - times_x * max_one_time_dis,
        abs(y) - times_y * max_one_time_dis,
    )
    #移动方向+-
    factor_x, factor_y = abs(x) // x, abs(y) // y

    for _ in range(times_x):
        dis = 125 * factor_x
        send_serial_msg(serial,mode=Mode.x_distance, x_dis=dis)
    #如果剩余距离>0.001
    if rest_x > 0.001:
        dis = factor_x * rest_x / max_one_time_dis * 125
        print(dis)
        send_serial_msg(serial,mode=Mode.x_dis_mm, x_dis=dis)
    else:
        pass

    for _ in range(times_y):
        dis = 125 * factor_y
        send_serial_msg(serial,mode=Mode.y_distance, y_dis=dis)
    if rest_y > 0.001:
        dis = factor_y * rest_y / max_one_time_dis * 125
        print(dis)
        send_serial_msg(serial,mode=Mode.y_dis_mm, y_dis=dis)
    else:
        pass

def move_in_mm(serial, x=0, y=0):
    x = 128 if x > 128 else int(x)
    x = -127 if x < -127 else int(x)
    y = 128 if y > 128 else int(y)
    y = -127 if y < -127 else int(y)
    if x != 0:
        send_serial_msg(serial,mode=Mode.x_dis_mm, x_dis=x)
    if y != 0:
        send_serial_msg(serial,mode=Mode.y_dis_mm, y_dis=y)

def grubBlockFromRawArea(serial):
    send_serial_msg(serial,mode=Mode.grub_1)

def grubBlockFromGround(serial):
    send_serial_msg(serial,mode=Mode.grub_2)

def putBlockToCircle(serial):
    send_serial_msg(serial,mode=Mode.down_1)

def putBlockToAnotherBlock(serial):
    send_serial_msg(serial,mode=Mode.down_2)

def adjustHeight(serial, target_height):
    heightConfigs = [mode for mode in HeightMode]
    if target_height not in heightConfigs:
        raise ValueError("小车高度模式中没有这个模式{0}".format(target_height))
    send_serial_msg(serial,mode=Mode.adjust_height, x_dis=target_height)

def handle_unknown_data(data):
    print("Received unknown data:", data)

def wait_for_movement_done(serial):
    while True:
            header = ord(serial.read())
            if header == send_byte[0]:
                if ord(serial.read()) == 0x01:
                    return True
                else:
                    pass
            else:
                pass

        
# 示例用法
if __name__ == "__main__":
    
    #wait_for_start()
    
    send_serial_msg(ser, Mode.rotate, angel=40)

    set_distance(ser,2,3)
    print("setOK")
    quit()
    receive_and_execute_tasks()  