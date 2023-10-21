import serial
import yaml
from enum import Enum
import time
import parameter
import threading

with open("config.yaml", 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

header = config["signal_values"]["header"]
tail = config["signal_values"]["tail"]

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
            
            print(received_data)
            if received_byte == bytes([config["signal_values"]["tail"]]):  # 检查数据帧的结束标志
                if len(received_data)-4 < 0:  #缺位
                    received_data = bytearray()  
                else:   #正常及多位
                    if received_data[len(received_data)-4] == 255:
                        parameter.Mode.task_detect = received_data[1]
                        parameter.Mode.color_detect = received_data[2]
                        print(time.strftime('Receive:%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                        print(received_data)
                received_data = bytearray()  # 重置接收数据
        
        time.sleep(0.1)
  
# 生成串口数据、发送数据
def send_serial_data(serial):
    send_data = send_byte
    if parameter.Mode.task_detect != 7:
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
    if parameter.Mode.task_detect == 7:

        send_data[1] = parameter.Mode.task_detect

        for i in range(6):
            send_data[i+2]=parameter.WiFi_Scan.task_number[i]

        send_data[8] =  0x00
        serial.write(send_data)
    print(time.strftime('Send:%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print(send_data)
    time.sleep(0.2)

def receive_thread(serial):
    while True:
        receive_serial_data(serial)
        
def send_thread(serial):
    
    while True:
        if parameter.Mode.task_detect is not 0:
            send_serial_data(serial)
        else:
            parameter.Object_Data.center = (0, 0)
        
def Serial_Start():
    ser = serial_init()
    receive_thread_obj = threading.Thread(target=receive_thread, args=(ser,))
    receive_thread_obj.daemon = True  # 设置线程为守护线程，这样主程序退出时会自动结束线程
    receive_thread_obj.start()
    print("Receive Thread Start!")
    
    send_thread_obj = threading.Thread(target=send_thread, args=(ser,))
    send_thread_obj.daemon = True  # 设置线程为守护线程，这样主程序退出时会自动结束线程
    send_thread_obj.start()
    print("Send Thread Start!")
