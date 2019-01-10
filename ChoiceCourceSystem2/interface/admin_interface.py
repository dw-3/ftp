from db import modules


def admin_register_interface(name, password):
    admin_obj = modules.Admin.get_obj_name(name)
    if admin_obj:
        return False, '用户已存在'
    else:
        modules.Admin(name, password)
        return True, '注册成功'


def admin_create_interface(admin, school_name, addr):
    obj = modules.School.get_obj_name(school_name)
    if obj:
        return False, '学校已存在'
    else:
        admin_obj = modules.Admin.get_obj_name(admin)
        admin_obj.create_school(school_name, addr)
        return True, '%s:%s 学校已创建' % (admin, school_name)


def admin_create_teacher_interface(admin, name, password=123):
    obj = modules.Teacher.get_obj_name(name)
    if obj:
        return False, '老师已存在'
    else:
        admin_obj = modules.Admin.get_obj_name(admin)
        admin_obj.create_teacher(name, password)
        return True, '%s:%s 老师已创建' % (admin, name)


def admin_create_couse_interface(admin, course_name, price, peroid, school_name):
    course_obj = modules.Course.get_obj_name(course_name)
    if course_obj:
        return False, '课程已存在'
    else:
        admin_obj = modules.Admin.get_obj_name(admin)
        admin_obj.create_course(course_name, price, peroid)
        school_obj = modules.School.get_obj_name(school_name)
        school_obj.add_course(course_name)
        return True, '%s:%s  课程已创建' % (admin, course_name)
