# class People:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def tell_info(self):
#         print('%s:%s' % (self.name, self.age))
#
#
# p = People('yilei', 18)
# p.tell_info()
# class People:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def tell_info(self):
#         print('%s:%s' % (self.name, self.age))
#
#     @classmethod
#     def cls(cls):
#         print(cls)
#
#     @staticmethod
#     def func1(x, y):
#         print(x, y)
#
#
# p = People('yilei', 18)
# p.tell_info()
# People.cls()
# People.func1(1,2)

# import os
#
# user_path = os.mkdir(r'C:\Users\lei.yi\PycharmProjects\yl_ftp\conf\2')
# print('%s目录创建成功' % user_path)

# import os
# try:
#     if os.listdir(r'C:\Users\lei.yi\PycharmProjects\yl_ftp\databases\home\yilei\6777'):
#         print('True')
#     else:
#         print('False')
# except Exception  as f:
#     print(f)
# import os
# size=os.path.getsize(r'C:\Users\lei.yi\PycharmProjects\yl_ftp\databases\home\yilei\test')
# print(size)
# import struct
#
# data = struct.pack('i', 456)
# print(struct.unpack('i',data)[0])
# import configparser
#
# config = configparser.ConfigParser()
# config.read(r'C:\Users\lei.yi\PycharmProjects\yl_ftp\conf\userinfo',encoding='utf-8')
# config.remove_option('yilei', 'quota')
# config.set('yilei', 'quota', '1024')
# config.write(open(r'C:\Users\lei.yi\PycharmProjects\yl_ftp\conf\userinfo', mode='wt'))
list1=[1,2,3]
print(list1[-1])