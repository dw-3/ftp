def common_auth(user_type):
    from core import admin, student, teacher
    def wapper1(func):
        def wapper2(*args, **kwargs):
            if user_type == 'admin':
                if not admin.admin_info['name']:
                    admin.admin_login()
                else:
                    return func(*args, **kwargs)
            elif user_type == 'student':
                if not student.student_info['student']:
                    student.student_login()
                else:
                    return func(*args, **kwargs)
            elif user_type == 'teacher':
                if not teacher.teacher_info['teacher']:
                    teacher.teacher_login()
                else:
                    return func(*args, **kwargs)
            else:
                pass

        return wapper2

    return wapper1
