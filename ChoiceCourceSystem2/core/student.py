from interface import common_interface, student_interface
from db import modules
from lib import common

student_info = {
    'student': None
}


def student_main():
    print('学生界面'.center(40, '-'))
    while True:
        print(
            '''
                1. 注册
                2. 登录
                3. 选择学校
                4. 选择课程
                5. 查看成绩
                6. 查看操作日志
                7. 查看课程信息
                q. 退出
            '''
        )
        choice_dict = {
            '1': student_register,
            '2': student_login,
            '3': choice_school,
            '4': check_course,
            '5': check_score,
            '6': check_log,
            '7': course_info,
        }
        choice = input('请选择：').strip()
        if choice == 'q': break
        if choice not in choice_dict: continue
        choice_dict[choice]()


def student_login():
    while True:
        if student_info['student']:
            print('用户已经登录')
            break
        name = input('请输入名字：').strip()
        password = input('请输入密码：').strip()
        if not name or not password: continue
        state, msg = common_interface.login_interface('student', name, password)
        if state:
            print(msg)
            student_info['student'] = name
            break
        else:
            print(msg)


def student_register():
    print('学生注册'.center(40, '-'))
    if student_info['student']:
        print('用户%s已经登录，无法注册' % (student_info['student']))
    else:
        name = input('请输入名字：').strip()
        password = input('请输入密码：').strip()
        if not name or not password: return
        state, msg = student_interface.student_register(name, password)
        if state:
            print(msg)
            return
        else:
            print(msg)
            return


@common.common_auth(user_type='student')
def choice_school():
    print('学生选择学校'.center(40, '-'))
    while True:
        for i, school_name in enumerate(common_interface.check_school()):
            print('学校代码是:%s,学校是%s' % (i, school_name))
        choice = input('请选择学校代码：').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice > len(common_interface.check_school()):
                print('选项不存在！')
                continue
        else:
            print('请输入整数')
            continue
        state, msg = student_interface.check_school_interface(student_info['student'], school_name)
        if state:
            print(msg)
            break
        else:
            print(msg)


@common.common_auth(user_type='student')
def check_score():
    print('学生查看分数'.center(40, '-'))
    state, msg = student_interface.check_score_inteface(student_info['student'])
    if state:
        print(msg)
    else:
        print(msg)


@common.common_auth(user_type='student')
def check_course():
    print('学生选择课程'.center(40, '-'))
    for i, course_name in enumerate(common_interface.check_course()):
        print('课程代码是%s，课程名是%s' % (i, course_name))
    while True:
        choice = input('请选择课程:').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice > len(common_interface.check_school()):
                print('选项不存在！')
                continue
            else:
                state, msg = student_interface.choice_course_interface(student_info['student'], course_name)
                if state:
                    print(msg)
                    break
                else:
                    print(msg)
        else:
            print('请输入整数')
            break


def check_log():
    pass


@common.common_auth(user_type='student')
def course_info():
    print('学员%s的课程详细信息'.center(40, '-') % (student_info['student']))
    state, msg = student_interface.tell_info_interface(student_info['student'])
    if state:
        print(msg)
    else:
        print(msg)
