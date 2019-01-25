import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
database_dir = os.path.join(base_dir, 'databases')
user_info_path = os.path.join(base_dir, 'conf', 'userinfo')
