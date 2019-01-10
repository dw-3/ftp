import os
from conf import settings
import pickle


def select(dir_name, obj_name):
    path_dir = os.path.join(settings.BASE_DB, dir_name)
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)
    obj_name = os.path.join(path_dir,obj_name)
    if os.path.exists(obj_name):
        with open(obj_name, mode='rb') as f:
            return pickle.load(f)
    else:
        return None


def save(obj):
    path_dir = os.path.join(settings.BASE_DB, obj.__class__.__name__.lower())
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)
    obj_name = os.path.join(path_dir, obj.name)
    with open(obj_name, mode='wb') as f:
        pickle.dump(obj, f)
