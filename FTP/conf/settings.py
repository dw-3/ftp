import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE=os.path.join(BASE_DIR,'database','home',) #用户属主目录
USER_DB=os.path.join(BASE_DIR,'user_db')  #用户账户数据库
PUBLIC=os.path.join(BASE_DIR,'database','public')


#===============下列代码与配置无关   为查询目录大小-----------------------
# for root, dirs, files in os.walk(DATABASE, topdown=False):
#     for name in files:
#         print(root,name)
#     for name in dirs:
#         print(root,name)

# for root, dirs, files in os.walk(DATABASE, topdown=False):
#     for name in files:
#         print(os.path.join(root, name))
#     for name in dirs:
#         print(os.path.join(root, name))
