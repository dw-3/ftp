import socket, hashlib, os, sys

BASE_DIR = os.path.dirname(__file__)
db_path = os.path.join(BASE_DIR, 'database')


def hash(password):
    s = hashlib.md5()
    s.update(password.encode('utf-8'))
    return s.hexdigest()


class FtpClient:
    '''ftp客户端'''

    def __init__(self, ip_port):
        self.ip_port = ip_port

    def __connect(self):
        '''连接服务器'''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ip_port)

    def __start(self):
        '''程序开始'''
        self.__connect()
        while True:
            '''认证'''
            name = input('用户名：').strip()
            pwd = input('密码：').strip()
            pwd = hash(pwd)
            user_dict = ('%s:%s' % (name, pwd))
            self.client.sendall(user_dict.encode('utf-8'))
            state = self.client.recv(1024).decode('utf-8')
            if state.split(':')[0] == 'True':
                print(state.split(':')[1])
                self.__interaction(name)
            else:
                print(state.split(':')[1])

    def __interaction(self, name):
        '''交互开始'''
        while True:
            cmd = input('[%s]>>:' % name).strip()
            if len(cmd) == 0: continue
            cmd_cmd = cmd.split()[0]  # 按照空格切分输入的命令
            if hasattr(self, cmd_cmd):  # 如果类中存在对应方法则执行
                func = getattr(self, cmd_cmd)
                func(cmd)
            else:
                print('< %s >不是内部或外部命令，也不是可运行的程序或批处理文件。'
                      '可查看帮助文档(help)' % cmd)

    def help(self, cmd):
        '''帮助命令'''
        self.client.sendall(cmd.encode('utf-8'))
        print(self.client.recv(1024).decode('utf-8'))

    def ls(self, cmd):
        '''查看当前路径文件命令'''
        self.client.sendall(cmd.encode('utf-8'))
        print(self.client.recv(2048).decode('gbk'))

    def pwd(self, cmd):
        '''显示当前路径命令'''
        self.client.sendall(cmd.encode('utf-8'))
        print(self.client.recv(1024).decode('utf-8'))

    def mkdir(self, cmd):
        '''创建目录'''
        self.client.sendall(cmd.encode('utf-8'))
        print(self.client.recv(1024).decode('utf-8'))

    def cd(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))
        print(self.client.recv(1024).decode('utf-8'))

    def get(self, cmd):
        '''下载'''
        self.client.sendall(cmd.encode('utf-8'))  # 1 交互
        res = self.client.recv(1024).decode('utf-8')  # 2 交互
        if res == 'exist':
            filename = cmd.split()[1]
            if os.path.isfile(db_path + r'\%s' % filename):  # 如果文件存在
                receive_size = os.stat(db_path + r'\%s' % filename).st_size  # 已接收文件大小
                self.client.sendall(('exist:%s' % receive_size).encode('utf-8'))  # 交互3发送状态和大小
                state = self.client.recv(1024).decode('utf-8')  # 分支交互1
                if state == 'yes':
                    print('文件续传成功，正在下载')
                else:
                    print('文件完整，无法进行下载')
                    return
            else:
                receive_size = 0  # 文件不存在时为0
                self.client.sendall('no:0'.encode('utf-8'))  # 交互3发送状态

            file_size = int(self.client.recv(1024).decode('utf-8'))  # 交互4接收文件大小
            self.client.sendall('receive'.encode('utf-8'))  # 交互5此交互其实多余，但是怕粘包
            with open(db_path + r'\%s' % filename, 'ab') as f:
                file_size += int(receive_size)  # 计算总文件大小
                m = hashlib.md5()  # MD5
                while receive_size < file_size:  # 接收文件大小 < 总文件大小
                    real_size = file_size - int(receive_size)  # 计算剩余大小
                    if real_size > 1024:
                        size = 1024
                    else:
                        size = real_size
                    data = self.client.recv(size)  # 交互6  开始循环接收文件
                    receive_size += len(data)
                    f.write(data)  # 追加写入
                    m.update(data)
                    self.__progress(receive_size, file_size)  # 进度条啦
                client_md5 = m.hexdigest()  # 客户端新文件MD5值
                server_md5 = self.client.recv(1024).decode('utf-8')  # 交互7  接收服务端文件MD5值
                if client_md5 == server_md5: print('\nmd5值相同，文件具有一致性，文件下载完成')
        else:
            print(res)

    def put(self, cmd):
        '''上传'''
        if len(cmd.split()) == 2:
            file_name = cmd.split()[1]
            file_path = db_path + r'\%s' % file_name
            if os.path.isfile(file_path):  # 客户端本地是否有文件
                self.client.sendall(cmd.encode('utf-8'))  # 交互1
                print(self.client.recv(1024).decode('utf-8'))  # 交互2收到确认通知
                file_size = os.stat(file_path).st_size  # 计算本地文件大小
                self.client.sendall(str(file_size).encode('utf-8'))  # 交互3发送文件大小
                res = self.client.recv(1024).decode('utf-8')  # 交互4接收确认信息和可用空间
                remain_size = int(res.split(':')[1])
                if res.split(':')[0] == 'yes':
                    print('开始上传，当前剩余空间%sM' % (round(remain_size / 1024000)))  # 四舍五入
                    with open(file_path, 'rb') as f:
                        m = hashlib.md5()
                        for line in f:
                            m.update(line)
                            send_size = f.tell()  # 返回文件的当前位置
                            self.client.sendall(line)  # 交互5for循环发送文件数据
                            self.__progress(send_size, file_size)
                    self.client.sendall(m.hexdigest().encode('utf-8'))  # 交互6发送本地文件MD5值
                    print(self.client.recv(1024).decode('utf-8'))  # 交互7 接收完成信息
                else:
                    print('空间不足哦，无法上传，当前剩余空间%sM' % (round(remain_size / 1024000)))
            else:
                print('< %s > 文件不存在哦' % file_name)
        else:
            print('< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd)

    def __progress(self, recv_size, data_size, width=70):
        ''' =========进度条啦没整明白==========
    # data_size = 9292
    # recv_size = 0
    # while recv_size < data_size:
    #     time.sleep(0.1)  # 模拟数据的传输延迟
    #     recv_size += 1024  # 每次收1024
    #
    #     percent = recv_size / data_size  # 接收的比例
    #     progress(percent, width=70)  # 进度条的宽度70'''
        percent = float(recv_size) / float(data_size)
        if percent >= 1:
            percent = 1
        show_str = ('[%%-%ds]' % width) % (int(width * percent) * '>')
        print('\r%s %d%%' % (show_str, int(100 * percent)), file=sys.stdout, flush=True, end='')


# print(FtpClient.__dict__)
if __name__ == '__main__':
    ip_port = ('127.0.0.1', 6666)
    client = FtpClient(ip_port)
    client._FtpClient__start()
