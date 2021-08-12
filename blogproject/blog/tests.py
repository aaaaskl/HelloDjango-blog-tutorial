import os
import pathlib
import random
import sys
from datetime import timedelta

import django
from django.utils import timezone

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
# BASE_DIR = back(back(os.path.abspath(__file__)))

print('当前文件的绝对路径:>>',pathlib.Path(__file__))
print(pathlib.Path(__file__).resolve().parent.parent)
base_dir = back(back(pathlib.Path(__file__)))
print('当前项目根目录:',base_dir)
sys.path.insert(0,base_dir)

print(sys.path)

# BASE_DIR = os.path.join(BASE_DIR,'blogproject')
# sys.path.append(BASE_DIR)
# print(sys.path)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "blogproject.settings")
    django.setup()

    from blog.models import Category, Post, Tag
    from comments.models import Comment
    from django.contrib.auth.models import User

    print('test compete')