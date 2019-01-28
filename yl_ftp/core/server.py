import socketserver
import struct
from modules import user
import subprocess
import os
import configparser
from conf import settings


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('客户端地址：', self.client_address)
        while True:
            try:
                user_dict = self.request.recv(1024)
                if not user_dict:
                    break
                user_dict = user_dict.decode('utf-8')
                state, msg, user_path, current_path, config, name = user.login(user_dict)
                self.state = state
                self.msg = msg
                self.user_path = user_path
                self.current_path = current_path
                self.config = config
                self.name = name
                res = '%s:%s' % (self.state, self.msg)
                if self.state:
                    print(res)
                    self.request.send(res.encode('utf-8'))
                else:
                    print(res)
                    self.request.send(res.encode('utf-8'))
                    continue
                while True:
                    cmd = self.request.recv(1024).decode('utf-8')
                    if len(cmd) == 0:
                        break
                    if hasattr(self, cmd.split()[0]):
                        func = getattr(self, cmd.split()[0])
                        if cmd.split()[0] == 'get' or cmd.split()[0] == 'cd' or \
                                cmd.split()[0] == 'put' or cmd.split()[0] == 'mkdir':
                            cmd = r'%s' % cmd
                            func(cmd)
                        else:
                            func(cmd.split()[0])
                    else:
                        res = '%s command not found,you can use help' % cmd
                        self.request.sendall(res.encode('utf-8'))
            except Exception as f:
                print(f)
                continue

    def help(self, cmd):
        cmd_dict = '''
                   -------------------------帮助文档----------------------------------
                     命令                     说明                    示例
                      cd             切换目录(public公共目录)     cd dirname(目录名称)
                      ls                 查看当前目录下所有文件          ls
                      pwd                   查看当前路径               pwd
                      get                    下载文件              get filename(文件名)
                      put                    上传文件              put filename(文件名)
                     mkdir               创建目录(当前路径下)       mkdir dirname(目录名)
               '''

        if cmd == 'help':
            res = '%s' % cmd_dict
            self.request.sendall(res.encode('utf-8'))
        else:
            res = '%s 用法错误' % cmd
            self.request.sendall(res.encode('utf-8'))

    def mkdir(self, cmd):
        if len(cmd.split()) == 2:
            cmd = cmd.split()[1]
            self.user_path = os.path.join(self.current_path, cmd)
            self.request.sendall(self.user_path.encode('utf-8'))
        else:
            res = '%s 命令错误' % cmd
            self.request.sendall(res.encode('utf-8'))

    def pwd(self, cmd):
        if len(cmd.split()) > 1:
            res = '%s 命令使用错误' % cmd
            self.request.sendall(res.encode('utf-8'))
        else:
            res = self.current_path
            self.request.sendall(res.encode('utf-8'))

    def cd(self, cmd):
        cmd = cmd.split()
        if len(cmd) == 2:
            if cmd[1] in os.listdir(self.current_path):
                self.current_path = os.path.join(self.current_path, cmd[1])
                self.request.sendall(self.current_path.encode('utf-8'))
            else:
                res = '%s 目录不存在' % cmd[1]
                self.request.sendall(res.encode('utf-8'))
        else:
            res = '%s 命令错误' % cmd
            self.request.sendall(res.encode('utf-8'))

    def ls(self, cmd):
        if len(cmd.split()) > 1:
            res = '%s 命令使用错误' % cmd
            self.request.sendall(res.encode('utf-8'))
        else:
            obj = subprocess.Popen(
                'dir %s' % self.current_path,
                shell=True,
                stdout=subprocess.PIPE,
            )
            res = obj.stdout.read()
            self.request.sendall(res)

    def get(self, cmd):
        cmd = cmd.split()
        if len(cmd) == 2:
            dir_path = os.path.join(self.current_path, cmd[1])
            self.file = dir_path
            if cmd[1] in os.listdir(self.current_path) and not os.path.isdir(dir_path):
                self.Sticky_Bag()
            else:
                res = '%s 资源不存在或者资源为目录，无法下载' % cmd[1]
                self.request.sendall(res.encode('utf-8'))
        else:
            res = '%s 命令错误' % cmd
            self.request.sendall(res.encode('utf-8'))

    def put(self, cmd):
        file_path = cmd.split()[1]
        file_name = file_path.split('\\')[-1]
        if not os.path.isdir(file_path) and os.path.exists(file_path):
            total_size = self.request.recv(4)
            unpack_total_size = struct.unpack('i', total_size)[0]
            if unpack_total_size < int(self.config.get(self.name, 'quota')):
                if unpack_total_size <= 1024:
                    data = self.request.recv(unpack_total_size).decode('utf-8')
                    file_name = os.path.join(self.current_path, file_name)
                    with open(file_name, mode='at', encoding='utf-8') as f:
                        f.write(data)
                else:
                    data = b''
                    recv_total_size = 0
                    while recv_total_size < unpack_total_size:
                        per_data = self.request.recv(1024)
                        recv_total_size += len(per_data)
                        data += per_data
                        data = data.decode('utf-8')
                        file_name = os.path.join(self.current_path, file_name)
                        with open(file_name, mode='at', encoding='utf-8') as f:
                            f.write(data)
                res = '%s 资源上传完成 ' % file_name
                print('2')
                remain_space = int(self.config.get(self.name, 'quota')) - unpack_total_size
                user_info_config = configparser.ConfigParser()
                user_info_config.read(settings.user_info_path, encoding='utf-8')
                user_info_config.remove_option(self.name, 'quota')
                user_info_config.set(self.name, 'quota', str(remain_space))
                user_info_config.write(open(settings.user_info_path, mode='wt'))
                print('1')
                self.request.sendall(res.encode('utf-8'))
                print('3')
            else:
                res = '磁盘空间不足'
                self.request.sendall(res.encode('utf-8'))
        else:
            res = '%s 文件不存在或者是一个目录 ' % file_path
            self.request.sendall(res.encode('utf-8'))

    def Sticky_Bag(self):
        '''解决粘包问题'''
        file_size = os.path.getsize(self.file)
        file_size_format = struct.pack('i', file_size)
        self.request.sendall(file_size_format)
        f = open(self.file, mode='rt', encoding='utf-8')
        self.request.sendall(f.read().strip('\n').encode('utf-8'))
        res = '%s资源下载完成' % self.file
        self.request.sendall(res.encode('utf-8'))
