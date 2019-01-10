from core import src
from interface import admin_interface, common_interface
from lib import common

admin_info = {
    'name': None
}


def admin_main():
    while True:
        print('管理员界面'.center(40, '-'))
        print(
            '''
            1 注册
            2 登录
            3 创建学校
            4 创建老师
            5 创建课程
            6 查看操作日志
            q 退出
            '''
        )
        choice_dict = {
            '1': admin_register,
            '2': admin_login,
            '3': create_school,
            '4': create_teacher,
            '5': create_course,
            '6': check_log
        }
        choice = input('请选择(管理员):').strip()
        if choice == 'q':
            break
        if choice not in choice_dict:
            continue
        choice_dict[choice]()


def admin_register():
    print('管理员注册'.center(40, '-'))
    if admin_info['name']:
        print('已登录！')
        return
    else:
        while True:
            name = input('请输入名字：').strip()
            password = input('请输入密码：').strip()
            password2 = input('确认密码：').strip()
            if not name or not password: continue
            if password == password2:
                state, msg = admin_interface.admin_register_interface(name,password)
                if state:
                    print(msg)
                    break
                else:
                    print(msg)
            else:
                print('密码2次不一样！')


def admin_login():
    while True:
        print('管理员登录'.center(40, '-'))
        if admin_info['name']:
            print('已经登录')
            return
        name = input('请输入名字:').strip()
        password = input('请输入密码:').strip()
        if not name or not password:
            continue
        else:
            state, msg = common_interface.login_interface('admin', name, password)
            if state:
                print(msg)
                admin_info['name'] = name
                break
            else:
                print(msg)


@common.common_auth(user_type='admin')
def create_school():
    print('管理员创建学校'.center(40, '-'))
    school_name = input('请输入学校名称：')
    addr = input('请输入学校地址：')
    if not school_name or not addr:
        return
    state, msg = admin_interface.admin_create_interface(admin_info['name'], school_name, addr)
    if state:
        print(msg)
    else:
        print(msg)


@common.common_auth(user_type='admin')
def create_teacher():
    print('管理员创建老师'.center(40, '-'))
    name = input('请输入名字：').strip()
    password = input('请输入密码：').strip()
    if not name or not password:
        return
    state, msg = admin_interface.admin_create_teacher_interface(admin_info['name'], name, password)
    if state:
        print(msg)
    else:
        print(msg)


@common.common_auth(user_type='admin')
def create_course():
    school_list = common_interface.check_school()
    print('管理员创建课程'.center(40, '-'))
    for i, school in enumerate(school_list):
        print('代码是:%s,学校是:%s' % (i, school))
    choice_school = input('请选择学校：').strip()
    if choice_school.isdigit():
        choice_school = int(choice_school)
        if choice_school > len(school_list): return
        name = input('请输入名称：').strip()
        price = input('请输入价格：').strip()
        period = input('请输入周期：').strip()
        if not name or not price or not period: return
        state, msg = admin_interface.admin_create_couse_interface(admin_info['name'], name, price, period,
                                                                  school_list[choice_school])
        if state:
            print(msg)
        else:
            print(msg)
    else:
        print('请输入整数！')


def check_log():
    pass
