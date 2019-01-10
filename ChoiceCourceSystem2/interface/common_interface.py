from db import modules
from conf import settings
import os


def login_interface(user_type, name, password):
    if user_type == 'admin':
        obj = modules.Admin.get_obj_name(name)
        if obj:
            if obj.password == password:
                return True, '%s:%s 登录成功' % (user_type, name)
            else:
                return False, '密码错误'
        else:
            return False, '用户不存在'
    elif user_type == 'teacher':
        obj = modules.Teacher.get_obj_name(name)
        if obj:
            if obj.password == password:
                return True, '登录成功'
            else:
                return False, '密码错误'
        else:
            return False, '用户不存在'
    elif user_type == 'student':
        obj = modules.Student.get_obj_name(name)
        if obj:
            if obj.password == password:
                return True, '登录成功'
            else:
                return False, '密码错误'
        else:
            return False, '用户不存在'
    else:
        return '模式不存在'


def check_school():
    school_base = os.path.join(settings.BASE_DB, 'school')
    school_all = os.listdir(school_base)
    return school_all


def check_course():
    from interface import student_interface
    from core import student
    return student_interface.check_school_course(student.student_info['student'])


def teacher_check_course():
    from conf import settings
    course_dir = os.path.join(settings.BASE_DB, 'course')
    return os.listdir(course_dir)


def teacher_check_student():
    from conf import settings
    student_dir = os.path.join(settings.BASE_DB, 'student')
    return os.listdir(student_dir)
