from django.urls import path
from student import views

urlpatterns = [

    # 查询某个学生的所有课程
    path('my_course_list/<int:s_id>/', views.MyCourseList.as_view(), name='my_course_list'),

    # 查询某个学生的所有课程通知
    path('my_course_notice_id/<int:s_id>/', views.MyCourseNotice.as_view(), name='my_notice'),

    # 根据课程id查询课程名称
    path('get_course_name/<int:c_id>/', views.GetCourseName.as_view(), name='get_course_name'),

    # 查询某个学生的所有系统通知
    path('my_system_notice_id/<int:s_id>/', views.MySystemNotice.as_view(), name='my_system_notice'),

    # 批量导入学生信息
    path('import_student/', views.ImportStudent.as_view(), name='import_student'),
    #
    # # 查询其他学生的所有收藏夹，s_id为查询者id，b_id为被查询者id
    # path('get_favoritename/<int:s_id>/<int:b_id>/', views.GetFavoriteName.as_view(), name='get_favoritename'),
    #
    # # 获得一个收藏夹的所有笔记
    # path('get_note_by_favoritename/<int:s_id>/<int:b_id>/<str:favoritename>/', views.GetNoteByFavoriteName.as_view(), name='get_note_by_favoritename'),
    #
    # # 用户收藏笔记
    # path('fav_note/<int:s_id>/<int:b_id>/', views.FavNote.as_view(), name='fav_note'),
    #
    # # 用户取消收藏笔记
    # path('unfav_note/<int:s_id>/<int:b_id>/', views.UnfavNote.as_view(), name='unfav_note'),
    #
    # # 用户点赞笔记
    # path('like_note/<int:s_id>/<int:b_id>/', views.LikeNote.as_view(), name='like_note'),

    # 用户关注学生
    path('follow_student/<int:s_id>/<int:b_id>/', views.FollowStudent.as_view(), name='follow_student'),

    # 用户取消关注学生
    path('unfollow_student/<int:s_id>/<int:b_id>/', views.UnfollowStudent.as_view(), name='unfollow_student'),

    # 查询某个学生的所有关注
    path('my_follow/<int:s_id>/', views.GetFollowing.as_view(), name='my_follow'),

    # 根据通知id查询通知内容
    path('get_information_content/<int:i_id>/', views.GetInformationContent.as_view(), name='get_information_content'),

    # 验证学生登录
    path('validate_login/', views.ValidateStudentLogin.as_view(), name='validate_login'),

    # 学生调整个人信息
    path('adjust_student_info/<int:s_id>/', views.AdjustStudentInfo.as_view(), name='adjust_student_info'),
]
