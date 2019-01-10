from core import student, admin, teacher

tag = True


def run():
    global tag
    while tag:
        print(
            '''
            1 管理员视图
            2 教师视图
            3 学生视图
            q 退出
            ''')
        choice = input('请输入:').strip()
        dic = {'1': admin.admin_main,
               '2': teacher.teacher_main,
               '3': student.student_main,
               }
        if choice == 'q':
            tag = False
            break
        if choice not in dic:
            continue
        dic[choice]()
