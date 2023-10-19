# This is a competition about intelligent handling trolley

### The CV_code is divided into three parts.

The first part is detection. It is important for the hole work. We use traditional vision for identification.First, we perform image preprocessing, according to different color thresholds, through the HSV method, separate blue, red and green, and use Gaussian filtering for image processing.

The second part is identification, after completing the color classification, we find the outline of the material or landmark for processing, and process and screen according to the actual situation.

The third part is the logical processing part of sending and receiving data, first, according to the received instructions, enter the mode of identifying materials or landmarks, and then, according to the color instructions, the identification, the identified data coordinates, color information to the stm32.

Hopefully, our code can give you some inspiration, and will not occurre bug.

## 1.Introduction
- File

|    Name   |      Function  | Description |
|    ---    |        ---     |    ---         |
|main.py|    识别/检测 |包括检测以及识别程序|
|parameter.py| 类   |需要的类参数|
|serialport.py|      串口     |定义与下位机的通信协议|
|config.yaml|参数文件        | 变量参数|

## 3.Environment

|Library | URL |  Description |
| ---    | --- | ---          |
OpenCV  |https://github.com/opencv/opencv/tree/4.6.0 \ https://github.com/opencv/opencv_contrib/tree/4.x | 编译时两个包放一块，注意编译时需传入指定参数 |
## 4.Boot-Start

"Boot startup, refer to this blog post at https://blog.csdn.net/qq_44989881/article/details/119777857."



# Part II

## main.py 详解 