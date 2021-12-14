from os import getcwd
from time import strftime
from queue import Queue
import socket
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def NetInit():
    # 获取本机ip
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("本机IP：" + ip + "   端口号：" + "5005")
    address = (ip, 5005)  # 服务端地址和端口
    s.bind(address)  # 绑定服务端地址和端口
    s.listen(3)


def send():
    power_loop = Draw
    conn, addr = s.accept()  # 返回客户端地址和一个新的 socket 连接
    print('[+] Connected with', addr)
    while True:
        print(1)
        data = conn.recv(1024)  # buffersize 等于 1024
        data = data.decode(encoding='gbk')
        if not data:
            break
        print('[Received]', data)
        power_loop.add(power_loop, data)
        power_loop.view(power_loop)


class Draw:
    x = []
    y = []
    temp = Queue()
    Time = 0
    hundreds = 0

    def __init__(self):
        pass

    def view(self):
        plt.ion()
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(18.5, 8)
        plt.clf()
        ax = plt.gca()
        x_major_locator = MultipleLocator(2)
        ax.xaxis.set_major_locator(x_major_locator)
        plt.title('powerloop', fontsize=24)
        # 设置图表标题和标题字号
        plt.tick_params(axis='both', which='major', labelsize=14)
        # 设置刻度的字号
        plt.xlabel('time', fontsize=14)
        # 设置x轴标签及其字号
        plt.ylabel('power', fontsize=14)
        plt.plot(self.x, self.y)
        print(self.x)
        print(self.y)
        plt.pause(0.1)
        plt.show()

    def add(self, data_y):
        with open(full_path,'a') as t:
            data = data_y.split('\r\n')
            for i in data:
                if not i == '':
                    i = float(i)
                    self.temp.put(i)
            while not self.temp.empty():
                self.Time = self.Time + 1
                if len(self.x) >= 40:
                    self.x.remove(self.x[0])
                if len(self.y) >= 40:
                    self.y.remove(self.y[0])
                if self.Time >= 100:
                    self.hundreds += 1
                    self.Time = self.Time - 100
                num = self.temp.get()
                t.write(str(self.hundreds * 100 + self.Time) + ' ' + str(num)+'\n')
                self.x.append(str(self.hundreds * 100) + "h" + str(self.Time))
                self.y.append(num)


if __name__ == "__main__":
    full_path = getcwd() + '\\' + 'my' + str(strftime("%H:%M:%S")).replace(':', '') + '.txt'
    f = open(full_path, 'a')
    NetInit()
    send()
