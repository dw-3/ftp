import socket
from modules.user import hash
import os
import struct
from conf import settings


class MyClient(object):
    def __init__(self):
        self.ip_port = ('127.0.0.1', 8081)

    def connect(self):
        self.client = socket.socket()
        self.client.connect(self.ip_port)

    def start(self):
        '''认证'''
        self.connect()
        while True:
            username = input('username:').strip()
            password = input('password:').strip()
            password = hash(password)
            if not username or not password:
                continue
            user_dict = ('%s:%s' % (username, password))
            self.client.sendall(user_dict.encode('utf-8'))
            res = self.client.recv(1024).decode('utf-8')
            if res.split(':')[0] == 'False':
                print(res)
                continue
            else:
                print(res)
                while True:
                    self.interaction()

    def interaction(self):
        '''交互'''
        cmd = input('请输入命令：').strip()
        cmd = r'%s' % cmd
        if hasattr(self, cmd.split()[0]):
            func = getattr(self, cmd.split()[0])
            if cmd.split()[0] == 'cd' or cmd.split()[0] == 'put' \
                    or cmd.split()[0] == 'mkdir':
                func(cmd)
            elif cmd.split()[0] == 'get':
                func(cmd)
                self.Sticky_Bag(cmd)
            else:
                func(cmd.split()[0])
            if cmd.split()[0] == 'ls':
                print(self.client.recv(1024).decode('gbk'))
            elif cmd.split()[0] == 'cd':
                user_path = self.client.recv(1024).decode('utf-8')
                if os.chdir(user_path):
                    print('%s切换成功' % user_path)
                else:
                    print('%s切换失败' % user_path)
            elif cmd.split()[0] == 'mkdir':
                user_path = self.client.recv(1024).decode('utf-8')
                if os.mkdir(user_path):
                    print('%s目录创建成功' % user_path)
                else:
                    print('%s目录创建失败' % user_path)
            else:
                print(self.client.recv(1024).decode('utf-8'))
        else:
            print('%s命令不存在' % cmd)

    def help(self, cmd):
        '''帮助'''
        self.client.sendall(cmd.encode('utf-8'))

    def ls(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))

    def cd(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))

    def pwd(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))

    def mkdir(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))

    def get(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))

    def Sticky_Bag(self, cmd):
        headers = self.client.recv(4)
        total_size = struct.unpack('i', headers)[0]
        put_path = os.path.join(settings.base_dir, 'get')
        resource = os.path.join(put_path, cmd.split()[1])
        recv_size = 0
        while recv_size < total_size:
            if total_size < 1024:
                per_recv_data = self.client.recv(total_size)
                recv_size = total_size
                f = open(resource, mode='at', encoding='utf-8')
                f.write(per_recv_data.decode('utf-8'))
                f.close()
            else:
                per_recv_data = self.client.recv(1024)
                recv_size += len(per_recv_data)
                f = open(resource, mode='at', encoding='utf-8')
                f.write(per_recv_data.decode('utf-8'))
                f.close()
        res = self.client.recv(1024).decode('utf-8')
        print(res)

    def put(self, cmd):
        self.client.sendall(cmd.encode('utf-8'))
        file_path = cmd.split()[1]
        total_size = os.path.getsize(file_path)
        pack_total_size = struct.pack('i', total_size)
        self.client.sendall(pack_total_size)
        with open(file_path, mode='rt', encoding='utf-8') as f:
            self.client.sendall(f.read().strip('\n').encode('utf-8'))
        print(self.client.recv(1024).decode('utf-8'))


if __name__ == '__main__':
    f = MyClient()
    f.start()
