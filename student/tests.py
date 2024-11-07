#编写接口的测试代码
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from global_models.models import *
from student.views import MyCourseList

from django.test import TestCase, RequestFactory
from .views import MyCourseList, MyCourseNotice, GetCourseMaterial, GetTest, GetExercise

from django.urls import reverse
#测试接口

#MyCourseList
class MyCourseListTestCase(TestCase):
    def setUp(self):
        # 此处用于填写测试数据,这个地方相当于创建了一个虚拟数据库

        # 创建测试用的学生
        self.student = Student.objects.create(name='Test Student',S_id=1)

        # 创建几个测试用的课程
        self.course1 = Course.objects.create(name='Math', C_id=1)
        self.course2 = Course.objects.create(name='Physics', C_id=2)
        self.course3 = Course.objects.create(name='Chemistry', C_id=3)

        # 将学生与课程关联起来
        StudentCourse.objects.create(S_id=self.student, C_id=self.course1)
        StudentCourse.objects.create(S_id=self.student, C_id=self.course2)

    def test_get_courses_for_student(self):
        # 创建一个RequestFactory对象，用于创建请求
        factory = RequestFactory()

        #创建request对象，请求的url为/student/1/courses/
        url = "/student/1/courses/"
        request = factory.get(url)

        #获取返回的response，MyCourseList.as_view()是直接调用
        response = MyCourseList.as_view()(request, s_id=self.student.S_id)


        #判断测试是否通过。断言 response的状态码是否为200，返回的数据中是否包含了Math和Physics两门课程
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['courses']), 2)
        self.assertEqual(response.data['courses'][0]['name'], 'Math')
        self.assertEqual(response.data['courses'][1]['name'], 'Physics')


