from django.urls import path

from teacher.views import *

urlpatterns = [
    #教师查看自己的课程
    path('<int:t_id>/courses/', GetCourse.as_view(), name='my_course_list'),
    #查看自己所交的课程的学生
    path('<int:t_id>/course-students/', GetCourseStudent.as_view(), name='my_course_student'),
    #修改课程介绍AdjustCourseInfo
    path('<int:t_id>/adjust-course-info/', AdjustCourseInfo.as_view(), name='adjust_course_info'),
    #修改课程大纲
    path('<int:t_id>/adjust-course-outline/', AdjustCourseOutline.as_view(), name='adjust_course_outline'),
    #修改教学日历
    path('<int:t_id>/adjust-course-calendar/', AdjustCourseCalendar.as_view(), name='adjust_course_calendar'),
    #查看课程大纲
    path('<int:t_id>/get-course-outline/', GetCourseOutline.as_view(), name='get_course_outline'),
    #查看教学日历
    path('<int:t_id>/get-course-calendar/', GetCourseCalendar.as_view(), name='get_course_calendar'),
    #查看课程介绍
    path('<int:t_id>/get-course-introduction/', GetCourseIntroduction.as_view(), name='get_course_introduction'),
    #创建课程通知，PublishNotice
    path('<int:t_id>/publish-notice/', PublishNotice.as_view(), name='publish_notice'),
    #教师登录
    path('login/', ValidateTeacherLogin.as_view(), name='validate_teacher_login'),
    #教师上传课件
    path('<int:t_id>/upload-courseware/', UploadTeachingMaterial.as_view(), name='upload_courseware'),
    #教师查看课件
    path('<int:t_id>/get-courseware/', GetCourseMaterial.as_view(), name='get_courseware'),
    #教师上传习题
    path('<int:t_id>/upload-exercise/', UploadExercise.as_view(), name='upload_exercise'),
    #教师查看习题
    path('<int:t_id>/get-exercise/', GetExercise.as_view(), name='get_exercise'),
    #教师上传试题
    path('<int:t_id>/upload-exam/', UploadTest.as_view(), name='upload_exam'),
    #教师查看试题
    path('<int:t_id>/get-exam/', GetTest.as_view(), name='get_exam'),
    #教师上传作业
    path('<int:t_id>/upload-work/', UploadWork.as_view(), name='upload_work'),
    #教师查看自己布置的作业
    path('<int:t_id>/get-work/', GetWork.as_view(), name='get_work'),
    #教师查看某个作业的提交情况
    path('<int:t_id>/work-students/', GetWorkSubmission.as_view(), name='work_student'),
    #教师查看某个学生的作业
    path('<int:t_id>/work-student/', GetStudentWork.as_view(), name='work_student'),
    #教师批改作业
    path('<int:t_id>/correct-work/', CorrectWork.as_view(), name='correct_work'),












]
