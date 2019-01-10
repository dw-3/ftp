from interface import teacher_interface, common_interface
from lib import common

teacher_info = {
    'teacher': None
}


def teacher_main():
    print('老师界面'.center(40, '-'))
    while True:
        print('''
                   1. 登录
                   2. 查看和选择课程
                   3. 查看学生
                   4. 修改学生成绩
                   5. 查看操作日志
                   q. 退出
                ''')
        choice = input('请输入选择：').strip()
        choice_dict = {
            '1': teacher_login,
            '2': view_course,
            '3': view_student,
            '4': set_stu_score,
            '5': check_log
        }
        if choice == 'q': break
        if choice not in choice_dict: continue
        choice_dict[choice]()


def teacher_login():
    print('老师登录'.center(40, '-'))
    while True:
        if teacher_info['teacher']:
            print('老师已经登录')
            return
        else:
            name = input('请输入名字：').strip()
            password = input('请输入密码：').strip()
            state, msg = common_interface.login_interface('teacher', name, password)
            if state:
                print(msg)
                teacher_info['teacher'] = name
                return
            else:
                print(msg)


@common.common_auth(user_type='teacher')
def view_course():
    while True:
        print('所有的课程如下:'.center(40, '-'))
        for i, course_name in enumerate(common_interface.teacher_check_course()):
            print('课程代码是%s,课程名称是%s' % (i, course_name))
        state, msg = teacher_interface.teacher_chooiced_course(teacher_info['teacher'])
        if state:
            print(msg)
        else:
            print(msg)
        choice = input('请选择课程代码:').strip()
        state, msg = teacher_interface.teacher_chooice_course(teacher_info['teacher'],
                                                              common_interface.teacher_check_course()[int(choice)])
        if state:
            print(msg)
            return
        else:
            print(msg)
            return


@common.common_auth(user_type='teacher')
def view_student():
    from interface import common_interface
    for i, student in enumerate(common_interface.teacher_check_student()):
        state, msg = teacher_interface.view_student_interface(teacher_info['teacher'], student)
        if state:
            print(msg)
        else:
            print(msg)


@common.common_auth(user_type='teacher')
def set_stu_score():
    print('老师设置学生分数'.center(40, '-'))
    state, msg = teacher_interface.set_score_interface(teacher_info['teacher'])
    if state:
        print(msg)
    else:
        print(msg)


def check_log():
    pass
