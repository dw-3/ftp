import socketserver, os, subprocess, hashlib
from modules.user import login
from conf import settings


class MyTcphandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            while True:
                '''认证开始'''
                user_dict = self.request.recv(1024).decode('utf-8')
                msg, tag, config, db_path, name = login(user_dict)  # 返回认证状态及数据
                self.config = config  # 为对象创建属性
                self.db_path = db_path  # 对象家目录
                self.now_path = db_path  # 对象当前路径
                self.name = name
                state = ('%s:%s' % (msg, tag))  # 认证状态
                if msg == False:
                    self.request.send(state.encode('utf-8'))
                    continue
                self.request.send(state.encode('utf-8'))
                while True:
                    '''交互开始'''
                    cmd = self.request.recv(1024).decode('utf-8')
                    if len(cmd) == 0: break
                    cmd_cmd = cmd.split()[0]  # 接收cmd命令按空格切分得到第一个值
                    if hasattr(self, cmd_cmd):  # 判断cmd命令存不存在类中
                        func = getattr(self, cmd_cmd)  # 字符串调用类方法
                        func(cmd)
        except Exception as f:  # 针对Windows
            print(f)

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
        if len(cmd.split()) > 1:
            res = '< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd
            self.request.sendall(res.encode('utf-8'))
        else:
            self.request.sendall(cmd_dict.encode('utf-8'))

    def ls(self, cmd):
        if len(cmd.split()) > 1:
            res = '< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd
            self.request.sendall(res.encode('utf-8'))
        else:
            obj = subprocess.Popen('dir %s' % self.now_path,
                                   shell=True,
                                   stdout=subprocess.PIPE
                                   )
            res = obj.stdout.read()
            self.request.sendall(res)

    def pwd(self, cmd):
        if len(cmd.split()) > 1:
            res = '< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd
        else:
            res = self.now_path
        self.request.sendall(res.encode('utf-8'))

    def mkdir(self, cmd):
        if len(cmd.split()) == 2:
            dir = cmd.split()[1]
            dir_path = self.now_path + r'\%s' % dir
            if not os.path.isdir(dir_path):  # 目录不存在
                os.mkdir(dir_path)
                res = '< %s >目录创建成功！！！' % dir
            else:
                res = '< %s >目录已存在！' % dir
        else:
            res = '< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd
        self.request.sendall(res.encode('utf-8'))

    def cd(self, cmd):
        if len(cmd.split()) == 2:
            dir = cmd.split()[1]
            if dir != self.name and dir in self.config.sections():
                res = '权限不足，不要瞎搞'

            elif dir == 'public':
                self.now_path = settings.PUBLIC
                res = '< pulic >共享目录切换成功！！！'

            elif os.path.isdir(self.now_path + r'\%s' % dir):
                self.now_path += r'\%s' % dir
                res = '< %s >目录切换成功！！！' % dir

            elif dir == '..' and len(self.now_path) > len(self.db_path):
                self.now_path = os.path.dirname(self.now_path)
                res = '< 上一级 >目录切换成功！！！'

            else:
                res = '权限不足，或路径不正确'
            self.request.sendall(res.encode('utf-8'))
        else:
            res = '< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd
            self.request.sendall(res.encode('utf-8'))

    def get(self, cmd):
        '''下载'''
        if len(cmd.split()) == 2:
            filename = cmd.split()[1]
            file_path = self.now_path + r'\%s' % filename
            if os.path.isfile(file_path):
                self.request.sendall('exist'.encode('utf-8'))  # 交互2发送文件存在的信号
                file_size = os.stat(file_path).st_size  # 计算文件大小
                res = self.request.recv(1024).decode('utf-8')  # 交互3接收状态信息
                if res.split(':')[0] == 'exist':  # 客户端文件存在
                    client_size = int(res.split(':')[1])

                    if client_size < file_size:  # 客户端文件支持续传
                        self.request.sendall('yes'.encode('utf-8'))  # 分支交互1
                        file_size -= client_size

                    else:
                        self.request.sendall('no'.encode('utf-8'))
                        return

                else:  # 文件不存在时
                    client_size = 0

                with open(file_path, 'rb') as f:
                    self.request.sendall(str(file_size).encode('utf-8'))  # 交互4发送文件大小
                    self.request.recv(1024)  # 交互5接收一次  其实多余 怕粘包
                    f.seek(client_size)  # 文件指针移动到客户端文件大小位置
                    m = hashlib.md5()
                    for line in f:
                        m.update(line)
                        self.request.sendall(line)  # 交互6for循环发送循环数据
                self.request.sendall(m.hexdigest().encode('utf-8'))  # 交互7发送服务端文件MD5值
            else:
                self.request.sendall('文件不存在哦'.encode('utf-8'))
        else:
            res = '< %s > 不是内部或外部命令，也不是可运行的程序或批处理文件,可查看帮助文档(help)' % cmd
            self.request.sendall(res.encode('utf-8'))

    def put(self, cmd):
        '''上传'''
        file_name = cmd.split()[1]
        file_path = self.now_path + r'\%s' % file_name
        self.request.sendall('已准备好上传服务'.encode('utf-8'))  # 交互2发送确认通知
        file_size = int(self.request.recv(1024).decode('utf-8'))  # 交互3接收文件大小
        quota_size = int(self.config.get(self.name, 'quota'))  # 拿到用户的磁盘配额
        used_size = self.__getdirsize(self.db_path)  # 计算得到用户已使用的空间
        remain_size = quota_size - used_size  # 得到用户剩余空间
        if file_size + used_size <= quota_size:
            self.request.sendall(('yes:%s' % remain_size).encode('utf-8'))  # 交互4发送可以接收通知和用户剩余空间
            with open(file_path, 'wb') as f:
                receive_size = 0
                m = hashlib.md5()
                while receive_size < file_size:
                    real_size = file_size - int(receive_size)  # 计算剩余大小
                    if real_size > 1024:
                        size = 1024
                    else:
                        size = real_size
                    data = self.request.recv(size)  # 交互5循环接收数据
                    receive_size += len(data)
                    f.write(data)
                    m.update(data)
                server_md5 = m.hexdigest()
                client_md5 = self.request.recv(1024).decode('utf-8')  # 交互6接收客户端文件MD5值
                if server_md5 == client_md5:
                    self.request.sendall('\nmd5值相同，文件具有一致性，文件上传完成'.encode('utf-8'))  # 交互7发送完成信息
        else:
            self.request.sendall(('no:%s' % remain_size).encode('utf-8'))  # 分支交互4

    def __getdirsize(self, db_path):
        '''计算已使用的用户家目录大小'''
        size = 0
        for root, dirs, files in os.walk(db_path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size
