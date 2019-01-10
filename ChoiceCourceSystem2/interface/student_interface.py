from db import modules


def student_register(name, password):
    obj = modules.Student.get_obj_name(name)
    if obj:
        return False, '用户已存在'
    else:
        modules.Student(name, password)
        return True, '学生：注册成功%s' % (name)


def check_school_interface(stu_name, school_name):
    obj = modules.Student.get_obj_name(stu_name)
    if obj.school:
        return False, '学生已经绑定学校,无法再次绑定'
    else:
        obj.add_school(school_name)
        return True, '学生:%s已经绑定学校:%s' % (stu_name, school_name)


def check_school_course(stu_name):
    obj_stu = modules.Student.get_obj_name(stu_name)
    obj_school = obj_stu.school
    obj_school2 = modules.School.get_obj_name(obj_school)
    obj_course = obj_school2.course_list
    print('学生%s所在学校为%s，可选课程为%s' % (stu_name, obj_school, obj_course))
    return obj_course


def choice_course_interface(stu_name, course_name):
    obj = modules.Student.get_obj_name(stu_name)
    if course_name in obj.course:
        return False, '%s课程已存在于%s' % (course_name, stu_name)
    else:
        obj.add_course(course_name)
        stu_course_all = obj.course
        return True, '学生%s本次绑定课程为%s,他的所有课程为%s' % (stu_name, course_name, stu_course_all)


def tell_info_interface(stu_name):
    obj_course_all = modules.Student.get_obj_name(stu_name)
    if obj_course_all:
        for i in obj_course_all.course:
            obj_per_course = modules.Course.get_obj_name(i)
            print('课程为%s,周期为%s,价格为%s' % (obj_per_course.name, obj_per_course.period, obj_per_course.price))
        return True, '课程信息如上！'.center(40, '-')
    else:
        return False, '学生%s未绑定课程' % (stu_name)


def check_score_inteface(student):
    obj = modules.Student.get_obj_name(student)
    if obj:
        return True, '学生分数如下%s' % (obj.course_score)
    else:
        return False, '学生不存在，无法查询分数'
