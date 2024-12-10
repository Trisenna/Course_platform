from django.urls import path
from .views import *
# 批量导入学生信息

urlpatterns = [
path('import/', ImportStudent.as_view(), name='import_student'),
]