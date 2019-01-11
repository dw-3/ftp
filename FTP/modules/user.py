from conf import settings
import os, configparser, hashlib


def login(user_dict):
    userlist = user_dict.split(':')
    name = userlist[0]
    password = userlist[1]
    config = query_db()  # 查询本地用户数据库
    if config.has_section(name):  # 判断有没有name
        true_name = config.get(name, 'name')  # 取出本地数据库对应name的名字
        true_pwd = hash(config.get(name, 'password'))  # 取出本地数据库对应name的加密过的密码
        if name == true_name and password == true_pwd:  # 比对
            db_path = os.path.join(settings.DATABASE + r'\%s' % name)
            return True, '恭喜%s,认证成功!!!' % name, config, db_path, name  # 额 返回了五个值。。。。

        else:
            return False, '用户名或密码错误', None, None, None

    else:
        return False, '用户不存在', None, None, None


def query_db():
    '''查询本地数据库'''
    config = configparser.ConfigParser()
    config.read(r'C:\Users\lei.yi\PycharmProjects\FTP\user_db\user.ini')

    return config


def hash(password):
    s = hashlib.md5()
    s.update(password.encode('utf-8'))
    return s.hexdigest()

