#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

// Define the structure to represent the data
struct SerialData {
    unsigned char header;
    unsigned char mode;
    char x_dis;
    char y_dis;
    char angel;
    unsigned char tail;
};

// Function to initialize the serial port
int initSerialPort(const char *port) {
    int fd;
    struct termios tty;

    fd = open(port, O_RDWR | O_NOCTTY);
    if (fd == -1) {
        perror("Error opening serial port");
        return -1;
    }

    memset(&tty, 0, sizeof(tty));
    if (tcgetattr(fd, &tty) != 0) {
        perror("Error from tcgetattr");
        return -1;
    }

    tty.c_cflag |= CREAD | CLOCAL;
    tty.c_cflag &= ~PARENB;
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;
    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    tty.c_iflag &= ~(IXON | IXOFF | IXANY);
    tty.c_oflag &= ~OPOST;

    cfsetispeed(&tty, B115200);
    cfsetospeed(&tty, B115200);

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        perror("Error from tcsetattr");
        return -1;
    }

    return fd;
}

// 定义数据包结构
struct SerialData_Report {
    unsigned char header;

    unsigned char status;
    unsigned char tail;
};



// 下位机函数：模拟动作并发送状态
void performActionAndSendStatus(int fd, unsigned char mode) {
    struct SerialData_Report response;
    response.header = 0xFF;
    response.tail = 0xFE;
    // 模拟执行动作...
    // 如果动作完成，设置状态为0x01；否则，设置状态为0x00

    // 检查动作是否完成的条件
    if (1) {
        response.status = 0x01; // 动作完成
        printf("Done\n");
    } else {
        response.status = 0x00; // 动作未完成
    }

    // 将响应数据包发送回上位机
    write(fd, &response, sizeof(response));
}



// Function to read and parse data from the serial port
void readAndParseData(int fd) {
    struct SerialData data;

    while (1) {
        int n = read(fd, &data, sizeof(data));
        if (n == sizeof(data)) {
            // Data received and parsed successfully
            if (data.mode == 0x01) {
                printf("Received Mode: x_distance, x_dis: %d\n", data.x_dis);
                performActionAndSendStatus(fd,data.mode);
                // Handle x_distance mode
            } else if (data.mode == 0x02) {
                printf("Received Mode: y_distance, y_dis: %d\n", data.y_dis);
                performActionAndSendStatus(fd,data.mode);
                // Handle y_distance mode
            } else if (data.mode == 0x03) {
                printf("Received Mode: rotate, angel: %d\n", data.angel);
                performActionAndSendStatus(fd,data.mode);
                // Handle rotate mode
            } 
            else if (data.mode == 0x05) {
                printf("Received Mode: x_mm, x_mm: %d\n", data.x_dis);
                performActionAndSendStatus(fd,data.mode);
                // Handle rotate mode
            }
            else if (data.mode == 0x06) {
                printf("Received Mode: y_mm, y_mm: %d\n", data.y_dis);
                performActionAndSendStatus(fd,data.mode);
                // Handle rotate mode
            }else {
                printf("Received unknown data\n");
                // Handle unknown data
            }
        } else {
            printf("Error reading data\n");
        }
    }
}



int main() {
    const char *serialPort = "/dev/pts/5"; // Change this to your serial port
    int fd = initSerialPort(serialPort);
    while (fd != -1) {
        readAndParseData(fd);

    }
    close(fd);
    return 0;
}
