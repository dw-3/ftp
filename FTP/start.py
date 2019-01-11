import socketserver, configparser, os, sys
from modules import server
from conf import settings


def create_dir():
    '''初始化生成本地数据库用户属主目录'''
    config = configparser.ConfigParser()  # configpasrser模块
    config.read(r'C:\Users\lei.yi\PycharmProjects\FTP\user_db\user.ini')  # 用户数据文件路径
    for user_name in config.sections():  # 循环取值
        user_path = settings.DATABASE + r'\%s' % user_name
        if not os.path.isdir(user_path):  # 文件夹不存在则创建
            os.mkdir(user_path)


if __name__ == '__main__':
    create_dir()
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 6666), server.MyTcphandler)
    server.serve_forever()
