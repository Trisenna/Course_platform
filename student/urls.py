from django.urls import path
from student import views
from student.views import *
urlpatterns = [

    path('<int:s_id>/courses/', MyCourseList.as_view(), name='my_course_list'),
    path('<int:s_id>/course-notices/', MyCourseNotice.as_view(), name='my_course_notice'),
    path('<int:s_id>/system-notices/', MySystemNotice.as_view(), name='my_system_notice'),
    path('import/', ImportStudent.as_view(), name='import_student'),
    path('<int:s_id>/follow/<int:b_id>/', FollowStudent.as_view(), name='follow_student'),
    path('<int:s_id>/following/', GetFollowing.as_view(), name='get_following'),
    path('<int:s_id>/unfollow/<int:b_id>/', UnfollowStudent.as_view(), name='unfollow_student'),
    path('<int:s_id>/adjust-info/', AdjustStudentInfo.as_view(), name='adjust_student_info'),
    path('login/', ValidateStudentLogin.as_view(), name='validate_student_login'),
    path('favorites/create/<int:s_id>/', CreateFavorite.as_view(), name='create_favorite'),
    path('favorites/fav/<int:s_id>/<int:b_id>/', FavFavorite.as_view(), name='fav_favorite'),
    path('favorites/unfav/<int:s_id>/', UnfavFavorite.as_view(), name='unfav_favorite'),
    path('favorites/unfav_id/<int:s_id>/<int:b_id>/', UnfavFavorite_id.as_view(), name='unfav_favorite_id'),
    path('favorites/like/<int:s_id>/<int:b_id>/', LikeFavorite.as_view(), name='like_favorite'),
    path('favorites/unlike/<int:s_id>/<int:b_id>/', UnlikeFavorite.as_view(), name='unlike_favorite'),
    path('favorites/isfav/<int:s_id>/<int:b_id>/', IsFavFavorite.as_view(), name='is_fav_favorite'),
    path('favorites/islike/<int:s_id>/<int:b_id>/', IsLikeFavorite.as_view(), name='is_like_favorite'),
    path('<int:s_id>/info/', GetStudentInfo.as_view(), name='get_student_info'),
    path('<int:s_id>/favorites/', GetFavorite.as_view(), name='get_favorite'),
    path('<int:s_id>/favorites/notes/', GetNoteInFavorite.as_view(), name='get_note_in_favorite'),
    path('<int:s_id>/favorites/<int:b_id>/', GetFavorite_other.as_view(), name='get_favorite_other'),
    path('<int:s_id>/favorites/<int:b_id>/notes/', GetNoteInFavorite_other.as_view(), name='get_note_in_favorite_other'),
    path('<int:s_id>/upload-note/', UploadNote.as_view(), name='upload_note'),
    path('<int:s_id>/delete-note/', DeleteNote.as_view(), name='delete_note'),
    path('<int:s_id>/download-note/', DownloadNote.as_view(), name='download_note'),
    path('<int:s_id>/download-note/<int:b_id>/', DownloadNote_other.as_view(), name='download_note_other'),






]
