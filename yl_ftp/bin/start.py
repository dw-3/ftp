from conf import settings
import configparser
import os
from core import server
import socketserver


def create_dir():
    user_path = os.path.join(settings.database_dir, 'home')
    config = configparser.ConfigParser()
    config.read(settings.user_info_path)
    for user_name in config.sections():
        if not os.path.exists(os.path.join(user_path, user_name)):
            os.mkdir(os.path.join(user_path, user_name))


if __name__ == '__main__':
    create_dir()
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8081), server.MyHandler)
    server.serve_forever()
