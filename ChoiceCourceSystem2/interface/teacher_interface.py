from db import modules


def teacher_chooiced_course(teacher_name):
    obj = modules.Teacher.get_obj_name(teacher_name)
    if obj.course:
        return True, '老师%s已经绑定的课程如下%s' % (teacher_name, obj.course)
    else:
        return False, '老师%s未绑定课程' % teacher_name


def teacher_chooice_course(teacher_name, course_name):
    obj = modules.Teacher.get_obj_name(teacher_name)
    if course_name in obj.course:
        return False, '老师%s已经绑定了课程%s,此次绑定失败' % (teacher_name, course_name)
    else:
        obj.add_course(course_name)
        return True, '老师%s已经成功绑定了课程%s' % (teacher_name, course_name)


def view_student_interface(teacher_name, student):
    obj_student = modules.Student.get_obj_name(student)
    obj_teacher = modules.Teacher.get_obj_name(teacher_name)
    if student in obj_teacher.student:
        return False, '学生%s之前已经绑定给老师%s' % (student, teacher_name)
    else:
        if set(obj_teacher.course) & set(obj_student.course):
            obj_teacher.add_student(student)
            return True, '学生%s此次绑定给老师%s' % (student, teacher_name)
        else:
            return False, '学生%s学的课程老师%s未备课！' % (student, teacher_name)


def set_score_interface(teacher_name):
    obj_teacher = modules.Teacher.get_obj_name(teacher_name)
    if obj_teacher.student:
        for i, student in enumerate(obj_teacher.student):
            obj_student = modules.Student.get_obj_name(student)
            print('老师的学生有%s,他的课程有%s' % (student, obj_student.course))
        student_name = input('请选择学生：').strip()
        student_course = input('请选择课程：').strip()
        student_score = input('请输入分数：').strip()
        obj_choice_student = modules.Student.get_obj_name(student_name)
        obj_choice_student.set_course_score(student_course, student_score)
        return True, '%s学生课程%s添加分数%s' % (student_name, student_course, student_score)
    else:
        return False, '无学生，无法添加分数'
