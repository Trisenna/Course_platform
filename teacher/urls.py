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


    # 用户查询个人信息
    path('<int:t_id>/info/', GetTeacherInfo.as_view(), name='get_teacher_info'),
    # 教师调整个人信息
    path('<int:t_id>/adjust-info/', AdjustTeacherInfo.as_view(), name='adjust_teacher_info'),
    # 教师查看课程的讨论区
    path('<int:t_id>/<int:c_id>/discuss/', GetDiscuss.as_view(), name='discuss'),
    # 教师在课程的讨论区发布帖子
    path('<int:t_id>/<int:c_id>/creatediscuss/', CreateDiscuss.as_view(), name='post_discuss'),
    # 用户对讨论区的帖子发表评论
    path('<int:t_id>/discuss/<int:d_id>/', CreateReply.as_view(), name='post_reply'),
    # 用户查看帖子的评论
    path('<int:t_id>/discuss/<int:d_id>/reply/', GetReply.as_view(), name='reply'),
    # 用户点赞帖子
    path('<int:t_id>/discuss/<int:d_id>/like-discuss/', LikeDiscuss.as_view(), name='like_discuss'),
    # 用户取消点赞帖子
    path('<int:t_id>/discuss/<int:d_id>/cancel-like-discuss/', CancelLikeDiscuss.as_view(), name='cancel_like_discuss'),
    # 用户点赞帖子的评论
    path('<int:t_id>/discuss/<int:d_id>/<int:r_id>/like-reply/', LikeDiscussReply.as_view(), name='like_reply'),
    # 用户取消点赞帖子的评论
    path('<int:t_id>/discuss/<int:d_id>/<int:r_id>/cancel-like-reply/', CancelLikeDiscussReply.as_view(), name='cancel_like_reply'),
    # 获取帖子的点赞数
    path('<int:t_id>/discuss/<int:d_id>/numOfLikes/', GetLikesOfDiscuss.as_view(), name='likes_of_discuss'),
    # 获取帖子的的评论的点赞数
    path('<int:t_id>/discuss/<int:d_id>/<int:r_id>/numOfLikes/', GetLikesOfReply.as_view(), name='likes_of_reply'),
    # 教师删除讨论区的帖子
    path('<int:t_id>/discuss/<int:d_id>/delete/', DeleteDiscuss.as_view(), name='delete_discuss'),
    # 教师删除讨论区帖子的评论
    path('<int:t_id>/discuss/<int:d_id>/<int:r_id>/delete/', DeleteReply.as_view(), name='delete_discuss_reply'),
    # 用户通过关键词模糊搜索帖子和评论的内容
    path('<int:t_id>/search/', SearchContent.as_view(), name='search_content'),
    # 查询某个教师的所有课程通知和被@的通知
    path('<int:t_id>/course-notices/', MyCourseNotice.as_view(), name='course_notices'),
    # 获取某课程的所有教师和用户
    path('<int:t_id>/<int:c_id>/allCourseUsers/', GetList.as_view(), name='get_all_course_users'),
    # 查询某个教师的所有系统通知
    path('<int:t_id>/system-notices/', MySystemNotice.as_view(), name='get_all_system_notices'),
    # 获取某课程讨论区的所有话题关键词
    path('<int:t_id>/<int:c_id>/allKeyWords/', GetKeyWords.as_view(), name='get_all_keywords'),
    # 处理用户发布帖子的关键词
    path('<int:t_id>/discuss/<int:d_id>/', DiscussKeyword.as_view(), name='discuss_keyword'),
    # 获取此课程讨论区含有目标关键词的所有帖子
    path('<int:t_id>/<int:c_id>/<int:k_id>/targetDiscuss/', GetALLTargetDiscuss.as_view(),name='get_all_target_discuss'),





]
