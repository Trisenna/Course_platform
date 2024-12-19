from django.urls import path
from .views import *
# 批量导入学生信息

urlpatterns = [
    path('import/', ImportStudent.as_view(), name='import_student'),
    path('import_teacher/', ImportTeacher.as_view(), name='import_teacher'),
    path('import_admin/', ImportAdmin.as_view(), name='import_admin'),
    # 教务处发布系统通知
    path('publish_system_notice/', PublishSystemNotice.as_view(), name='publish_system_notice'),
    # 获取所有的学生和教师
    path('get_all_users/', GetAllUsers.as_view(), name='get_all_users'),
]