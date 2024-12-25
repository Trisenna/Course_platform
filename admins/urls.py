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
    # 查询所有课程
    path('get_all_courses/', GetAllCourses.as_view(), name='get_all_courses'),
    # 创建课程
    path('create_course/', CreateCourse.as_view(), name='create_course'),
    # 为课程添加学生和教师
    path('add_course_user/', AddCourseUser.as_view(), name='add_course_user'),
    # 删除课程
    path('delete_course/', DeleteCourse.as_view(), name='delete_course'),
    # 获取某个课程的所有学生
    path('get_course_students/<int:c_id>/', GetCourseStudents.as_view(), name='get_course_students'),
    # 获取某个课程的所有教师
    path('get_course_teachers/<int:c_id>/', GetCourseTeachers.as_view(), name='get_course_teachers'),
    # 修改某个课程的课程信息
    path('modify_course/<int:c_id>/', ModifyCourse.as_view(), name='modify_course'),
]