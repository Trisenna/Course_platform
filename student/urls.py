from django.urls import path

from student import views

urlpatterns = [
    path('my_course_list/<int S_id>/', views.my_course_list, name='my_course_list'),
]
