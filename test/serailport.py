import serial
import yaml
from enum import Enum
import time
import parameter


with open("config.yaml", 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


header = config["signal_values"]["header"]
tail = config["signal_values"]["tail"]

# signal_values:
#   header: 0xFF
#   mode: 0x00
#   x_pos_1: 0x00
#   x_pos_2: 0x00
#   x_pos_3: 0x00
#   y_pos_1: 0x00
#   y_pos_2: 0x00
#   y_pos_3: 0x00
#   color: 0x00
#   tail: 0xFE

send_byte = bytearray([config["signal_values"]["header"], 
                       config["signal_values"]["mode"], 
                       config["signal_values"]["x_pos_1"],
                       config["signal_values"]["x_pos_2"],
                       config["signal_values"]["x_pos_3"],
                       config["signal_values"]["y_pos_1"],
                       config["signal_values"]["y_pos_2"],
                       config["signal_values"]["y_pos_3"], 
                       config["signal_values"]["color"], 
                       config["signal_values"]["tail"]])

receive_byte = bytearray([config["signal_values"]["header"], 
                          config["signal_values"]["mode"], 
                          config["signal_values"]["color"], 
                          config["signal_values"]["tail"]])

def serial_init():
    ser = serial.Serial(port=config["serial_config"]["port"],
                        baudrate=config["serial_config"]["baudrate"],
                        bytesize=config["serial_config"]["bytesize"],
                        parity = {
                            "none": serial.PARITY_NONE,
                            "odd": serial.PARITY_ODD,
                            "even": serial.PARITY_EVEN}[config["serial_config"]["parity"]],
                        stopbits=config["serial_config"]["stopbits"])  # open serial port
    return ser

# 定义接收数据的处理函数
def receive_serial_data(ser):
    received_data = bytearray()  # 用于存储接收到的数据

    while True:
        if ser.in_waiting > 0:  # 检查是否有可用的数据

            received_byte = ser.read(1)  # 读取一个字节

            if received_byte == bytes([config["signal_values"]["header"]]):  # 检查数据帧的起始标志
                received_data = bytearray()  # 重新初始化接收数据
            received_data.extend(received_byte)  # 将接收的字节添加到数据中
            if received_byte == bytes([config["signal_values"]["tail"]]):  # 检查数据帧的结束标志
                parameter.Mode.task_detect = received_data[1]
                parameter.Mode.color_detect = received_data[2]
                print(time.strftime('Receive:%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                print(received_data)
                received_data = bytearray()  # 重置接收数据
                
        time.sleep(0.2)

    
# 生成串口数据、发送数据并等待回传结果
def send_serial_data(serial):
    send_data = send_byte
    center = parameter.Object_Data.center
    print(center)
    color = parameter.Mode.color_detect
    center0 = center[0]
    center1 = center[1]
    send_data[1] = parameter.Mode.task_detect

    send_data[2] = center0 & 0xFF
    send_data[3] = (center0 >> 8) & 0xFF
    send_data[4] = (center0 >> 16) & 0xFF
    send_data[5] = (center1 & 0xFF)
    send_data[6] = ((center1 >> 8) & 0xFF)
    send_data[7] = ((center1 >> 16) & 0xFF)

    send_data[8] =  color
    
    serial.write(send_data)
    
    print(time.strftime('Send:%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print(send_data)
    time.sleep(0.3)

def receive_thread(serial):
    while True:
        receive_serial_data(serial)
        
def send_thread(serial):
    while True:
        send_serial_data(serial)
def send_thread_2(serial):
    while True:
        send_serial_data_2(serial)
# 生成串口数据、发送数据并等待回传结果
def send_serial_data_2(serial):
    send_data = receive_byte
    
    send_data[1] = 0x03

    send_data[2] = 0x06
    
    serial.write(send_data)
    
    print(time.strftime('Send:%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print(send_data)
    time.sleep(1.5)
# 示例用法
# if __name__ == "__main__":
#      # 启动接收数据的线程
#        ser = serial_init()
#        while True:
#            send_serial_data(ser)
       
       #receive_thread(ser)
#     receive_serial_data(ser=serial_init())
#     receive_thread = threading.Thread(target=receive_thread, args=(ser,))
#     receive_thread.daemon = True  # 设置线程为守护线程，这样主程序退出时会自动结束线程
#     receive_thread.start()
#     while True:
#         send_serial_data(ser)

