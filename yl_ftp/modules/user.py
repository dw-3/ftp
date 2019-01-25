import configparser
from conf import settings
import hashlib
import os


def login(user_dict):
    username = user_dict.split(':')[0]
    password = user_dict.split(':')[1]
    config = query_db()
    if config.has_section(username):
        true_name = config.get(username, 'name')
        true_password = hash(config.get(username, 'password'))
        user_path = os.path.join(settings.database_dir, 'home', true_name)
        if true_password == password:
            return True, '%s认证成功' % username, user_path, user_path, config, true_name
        else:
            return False, '%s密码错误' % username, None, None, None, None

    else:
        return False, '用户%s不存在' % username, None, None, None, None


def query_db():
    config = configparser.ConfigParser()
    config.read(settings.user_info_path, encoding='utf-8')
    return config


def hash(password):
    s = hashlib.md5()
    s.update(password.encode('utf-8'))
    return s.hexdigest()


query_db().remove_option('yilei', 'quota')
query_db().write(open(settings.user_info_path, mode='wt'))