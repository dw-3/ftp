from db import db_handler


class BaseClass:
    def save(self):
        return db_handler.save(self)

    @classmethod
    def get_obj_name(cls, name):
        return db_handler.select(cls.__name__.lower(), name)


class Admin(BaseClass):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.save()

    def create_school(self, name, addr):
        School(name, addr)

    def create_teacher(self, name, password):
        Teacher(name, password)

    def create_course(self, name, price, period):
        Course(name, price, period)


class School(BaseClass):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.course_list = []
        self.save()

    def add_course(self, course_name):
        self.course_list.append(course_name)
        self.save()


class Teacher(BaseClass):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.course = []
        self.student = []
        self.save()

    def add_course(self, course_name):
        self.course.append(course_name)
        self.save()

    def add_student(self, student_name):
        self.student.append(student_name)
        self.save()


class Student(BaseClass):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.school = None
        self.course = []
        self.score = []
        self.course_score = {}
        self.save()

    def add_school(self, school_name):
        self.school = school_name
        self.save()

    def add_course(self, course_name):
        self.course.append(course_name)
        self.save()

    def set_score(self, score):
        self.score.append(score)
        self.save()

    def set_course_score(self, course, score):
        self.course_score.update({course: score})
        self.save()




class Course(BaseClass):
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period
        self.save()
