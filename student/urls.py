from django.urls import path
from student import views
from student.views import *
urlpatterns = [
    #查看自己的课程
    path('<int:s_id>/courses/', MyCourseList.as_view(), name='my_course_list'),
    #查看自己的课程的通知
    path('<int:s_id>/course-notices/', MyCourseNotice.as_view(), name='my_course_notice'),
    #查看自己的系统通知
    path('<int:s_id>/system-notices/', MySystemNotice.as_view(), name='my_system_notice'),

    # 增加学生关注学生
    path('<int:s_id>/follow/<int:b_id>/', FollowStudent.as_view(), name='follow_student'),
# 获得学生关注的学生
    path('<int:s_id>/following/', GetFollowing.as_view(), name='get_following'),
# 获得学生关注的学生
    path('<int:s_id>/unfollow/<int:b_id>/', UnfollowStudent.as_view(), name='unfollow_student'),

# 学生调整个人信息
    path('<int:s_id>/adjust-info/', AdjustStudentInfo.as_view(), name='adjust_student_info'),
# 验证学生登录
    path('favorites/create/<int:s_id>/', CreateFavorite.as_view(), name='create_favorite'),
# 用户收藏其他人的收藏夹
    path('favorites/fav/<int:s_id>/<int:b_id>/', FavFavorite.as_view(), name='fav_favorite'),
# 用户收藏其他人的收藏夹
    path('favorites/unfav/<int:s_id>/', UnfavFavorite.as_view(), name='unfav_favorite'),
#用户删除收藏的收藏夹
    path('favorites/unfav_id/<int:s_id>/<int:b_id>/', UnfavFavorite_id.as_view(), name='unfav_favorite_id'),
#用户删除收藏的收藏夹
    path('favorites/like/<int:s_id>/<int:b_id>/', LikeFavorite.as_view(), name='like_favorite'),
#用户删除收藏的收藏夹
    path('favorites/unlike/<int:s_id>/<int:b_id>/', UnlikeFavorite.as_view(), name='unlike_favorite'),
#判断用户是否收藏了某个用户的收藏夹
    path('favorites/isfav/<int:s_id>/<int:b_id>/', IsFavFavorite.as_view(), name='is_fav_favorite'),
#判断用户是否点赞了某个用户的收藏夹
    path('favorites/islike/<int:s_id>/<int:b_id>/', IsLikeFavorite.as_view(), name='is_like_favorite'),
#用户查询个人信息
    path('<int:s_id>/info/', GetStudentInfo.as_view(), name='get_student_info'),
#查看自己的收藏夹
    path('<int:s_id>/favorites/', GetFavorite.as_view(), name='get_favorite'),
#查看自己的收藏夹
    path('<int:s_id>/favorites/notes/', GetNoteInFavorite.as_view(), name='get_note_in_favorite'),
#用户获取他人的收藏夹
    path('<int:s_id>/favorites/<int:b_id>/', GetFavorite_other.as_view(), name='get_favorite_other'),
#用户获取他人的收藏夹中的笔记title
    path('<int:s_id>/favorites/<int:b_id>/notes/', GetNoteInFavorite_other.as_view(), name='get_note_in_favorite_other'),
#用户上传笔记
    path('<int:s_id>/upload-note/', UploadNote.as_view(), name='upload_note'),
#用户删除笔记
    path('<int:s_id>/delete-note/', DeleteNote.as_view(), name='delete_note'),
#用户下载自己的笔记
    path('<int:s_id>/download-note/', DownloadNote.as_view(), name='download_note'),
#用户下载他人的笔记
    path('<int:s_id>/download-note/<int:b_id>/', DownloadNote_other.as_view(), name='download_note_other'),
#学生查看课程的课程日历
    path('<int:s_id>/course-calendar/', GetCourseCalendar.as_view(), name='course_calendar'),
#学生查看课程的课成大纲
    path('<int:s_id>/course-outline/', GetCourseOutline.as_view(), name='course_outline'),
#学生查看课程的课程介绍
    path('<int:s_id>/course-introduction/', GetCourseIntroduction.as_view(), name='course_introduction'),

#学生查看课程的教师信息
    path('<int:s_id>/course-teacher/', GetCourseTeacherInfo.as_view(), name='course_teacher'),
#学生查看课程的课件
    path('<int:s_id>/courseware/', GetCourseMaterial.as_view(), name='course_material'),
#学生查看课程的习题
    path('<int:s_id>/exercise/', GetExercise.as_view(), name='exercise'),
#学生查看课程的试题
    path('<int:s_id>/exam/', GetTest.as_view(), name='exam'),
#学生查看课程的作业
    path('<int:s_id>/allwork/', GetAllwork.as_view(), name='work'),
#学生查看某个作业
    path('<int:s_id>/work/', GetWork.as_view(), name='one_work'),
#学生提交作业
    path('<int:s_id>/upload-work/', SubmitWork.as_view(), name='upload_work'),


    # 学生查看课程的讨论区
    path('<int:s_id>/<int:c_id>/discuss/', GetDiscuss.as_view(), name='discuss'),
    # 学生在课程的讨论区发布帖子
    path('<int:s_id>/<int:c_id>/creatediscuss/', CreateDiscuss.as_view(), name='post_discuss'),
    # 用户对讨论区的帖子发表评论
    path('<int:s_id>/discuss/<int:d_id>/', CreateReply.as_view(), name='post_reply'),
    # 用户查看帖子的评论
    path('<int:s_id>/discuss/<int:d_id>/reply/', GetReply.as_view(), name='reply'),
    # 用户点赞帖子
    path('<int:s_id>/discuss/<int:d_id>/like-discuss/', LikeDiscuss.as_view(), name='like_discuss'),
    # 用户取消点赞帖子
    path('<int:s_id>/discuss/<int:d_id>/cancel-like-discuss/', CancelLikeDiscuss.as_view(), name='cancel_like_discuss'),
    # 用户点赞帖子的评论
    path('<int:s_id>/discuss/<int:d_id>/<int:r_id>/like-reply/', LikeDiscussReply.as_view(), name='like_reply'),
    # 用户取消点赞帖子的评论
    path('<int:s_id>/discuss/<int:d_id>/<int:r_id>/cancel-like-reply/', CancelLikeDiscussReply.as_view(), name='cancel_like_reply'),
    # 获取帖子的点赞数
    path('<int:s_id>/discuss/<int:d_id>/numOfLikes/', GetLikesOfDiscuss.as_view(), name='likes_of_discuss'),
    # 获取帖子的的评论的点赞数
    path('<int:s_id>/discuss/<int:d_id>/<int:r_id>/numOfLikes/', GetLikesOfReply.as_view(), name='likes_of_reply'),
    # 用户通过关键词模糊搜索帖子和评论的内容
    path('<int:s_id>/search/', SearchContent.as_view(), name='search_content'),
    # 获取某课程的所有教师和学生
    path('<int:s_id>/<int:c_id>/allCourseUsers/', GetList.as_view(), name='get_all_course_users'),
    # 获取某课程讨论区的所有话题关键词
    path('<int:s_id>/<int:c_id>/allKeyWords/', GetKeyWords.as_view(), name='get_all_keywords'),
    # 处理用户发布帖子的关键词
    path('<int:s_id>/discuss/<int:d_id>/', DiscussKeyword.as_view(), name='discuss_keyword'),
    # 获取此课程讨论区含有目标关键词的所有帖子
    path('<int:s_id>/<int:c_id>/<int:k_id>/targetDiscuss/', GetALLTargetDiscuss.as_view(), name='get_all_target_discuss'),
]
