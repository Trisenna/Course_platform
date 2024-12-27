# #编写接口的测试代码
# from django.test import TestCase, RequestFactory
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from global_models.models import *
# from student.views import MyCourseList
#
# from django.test import TestCase, RequestFactory
# from .views import MyCourseList, MyCourseNotice, GetCourseMaterial, GetTest, GetExercise
#
# from django.urls import reverse
# #测试接口
#
# #MyCourseList
# class MyCourseListTestCase(TestCase):
#     def setUp(self):
#         # 此处用于填写测试数据,这个地方相当于创建了一个虚拟数据库
#
#         # 创建测试用的学生
#         self.student = Student.objects.create(name='Test Student',S_id=1)
#
#         # 创建几个测试用的课程
#         self.course1 = Course.objects.create(name='Math', C_id=1)
#         self.course2 = Course.objects.create(name='Physics', C_id=2)
#         self.course3 = Course.objects.create(name='Chemistry', C_id=3)
#
#         # 将学生与课程关联起来
#         StudentCourse.objects.create(S_id=self.student, C_id=self.course1)
#         StudentCourse.objects.create(S_id=self.student, C_id=self.course2)
#
#     def test_get_courses_for_student(self):
#         # 创建一个RequestFactory对象，用于创建请求
#         factory = RequestFactory()
#
#         #创建request对象，请求的url为/student/1/courses/
#         url = "/student/1/courses/"
#         request = factory.get(url)
#
#         #获取返回的response，MyCourseList.as_view()是直接调用
#         response = MyCourseList.as_view()(request, s_id=self.student.S_id)
#
#
#         #判断测试是否通过。断言 response的状态码是否为200，返回的数据中是否包含了Math和Physics两门课程
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data['courses']), 2)
#         self.assertEqual(response.data['courses'][0]['name'], 'Math')
#         self.assertEqual(response.data['courses'][1]['name'], 'Physics')
#
#
import pandas as pd
import matplotlib.pyplot as plt

# Define the structure of the project and estimated time for each feature (in hours)
project_structure = [
    {"Module": "本科生院管理页面", "Feature": "批量注册", "Subfeature": "读取Excel表格", "Hours": 10},
    {"Module": "本科生院管理页面", "Feature": "批量注册", "Subfeature": "教职工注册", "Hours": 8},
    {"Module": "本科生院管理页面", "Feature": "批量注册", "Subfeature": "学生注册", "Hours": 8},
    {"Module": "本科生院管理页面", "Feature": "发布通知", "Subfeature": "发布通知", "Hours": 5},

    {"Module": "学生用户主页", "Feature": "通知箱", "Subfeature": "查看通知", "Hours": 6},
    {"Module": "学生用户主页", "Feature": "课程列表", "Subfeature": "查看课程详情", "Hours": 12},
    {"Module": "学生用户主页", "Feature": "收藏夹", "Subfeature": "创建收藏夹", "Hours": 6},
    {"Module": "学生用户主页", "Feature": "收藏夹", "Subfeature": "修改收藏夹", "Hours": 6},
    {"Module": "学生用户主页", "Feature": "收藏夹", "Subfeature": "查看收藏夹", "Hours": 6},
    {"Module": "学生用户主页", "Feature": "个人信息", "Subfeature": "查看个人信息", "Hours": 4},
    {"Module": "学生用户主页", "Feature": "个人信息", "Subfeature": "修改个人信息", "Hours": 4},

    {"Module": "学生课程页面", "Feature": "课程考核", "Subfeature": "查看作业", "Hours": 10},
    {"Module": "学生课程页面", "Feature": "课程考核", "Subfeature": "提交作业", "Hours": 12},
    {"Module": "学生课程页面", "Feature": "课程考核", "Subfeature": "参加考试", "Hours": 14},
    {"Module": "学生课程页面", "Feature": "课程考核", "Subfeature": "查看成绩", "Hours": 6},
    {"Module": "学生课程页面", "Feature": "课程资源", "Subfeature": "课件", "Hours": 10},
    {"Module": "学生课程页面", "Feature": "课程资源", "Subfeature": "历年试卷", "Hours": 8},
    {"Module": "学生课程页面", "Feature": "课程资源", "Subfeature": "习题", "Hours": 8},
    {"Module": "学生课程页面", "Feature": "课程基础信息", "Subfeature": "查看课程介绍", "Hours": 6},
    {"Module": "学生课程页面", "Feature": "讨论区", "Subfeature": "发布帖子", "Hours": 10},
    {"Module": "学生课程页面", "Feature": "讨论区", "Subfeature": "查看帖子", "Hours": 12},
    {"Module": "学生课程页面", "Feature": "讨论区", "Subfeature": "搜索帖子", "Hours": 8},

    {"Module": "教师用户主页", "Feature": "通知箱", "Subfeature": "查看通知", "Hours": 5},
    {"Module": "教师用户主页", "Feature": "课程列表", "Subfeature": "查看课程", "Hours": 10},
    {"Module": "教师用户主页", "Feature": "收藏夹", "Subfeature": "修改收藏夹", "Hours": 6},
    {"Module": "教师用户主页", "Feature": "收藏夹", "Subfeature": "创建收藏夹", "Hours": 6},
    {"Module": "教师用户主页", "Feature": "收藏夹", "Subfeature": "查看收藏夹", "Hours": 6},
    {"Module": "教师用户主页", "Feature": "个人信息", "Subfeature": "查看个人信息", "Hours": 4},
    {"Module": "教师用户主页", "Feature": "个人信息", "Subfeature": "修改个人信息", "Hours": 4},

    {"Module": "教师课程主页", "Feature": "课程考核", "Subfeature": "查看学生作业", "Hours": 10},
    {"Module": "教师课程主页", "Feature": "课程考核", "Subfeature": "发布作业", "Hours": 10},
    {"Module": "教师课程主页", "Feature": "课程考核", "Subfeature": "发布考试", "Hours": 14},
    {"Module": "教师课程主页", "Feature": "课程考核", "Subfeature": "查看试卷", "Hours": 8},
    {"Module": "教师课程主页", "Feature": "课程考核", "Subfeature": "发布成绩", "Hours": 8},
    {"Module": "教师课程主页", "Feature": "课程资源", "Subfeature": "课件", "Hours": 10},
    {"Module": "教师课程主页", "Feature": "课程资源", "Subfeature": "历年试卷", "Hours": 8},
    {"Module": "教师课程主页", "Feature": "课程资源", "Subfeature": "习题", "Hours": 8},
    {"Module": "教师课程主页", "Feature": "课程基础信息", "Subfeature": "课程介绍", "Hours": 8},
    {"Module": "教师课程主页", "Feature": "讨论区", "Subfeature": "发布帖子", "Hours": 10},
    {"Module": "教师课程主页", "Feature": "讨论区", "Subfeature": "查看帖子", "Hours": 10},
    {"Module": "教师课程主页", "Feature": "讨论区", "Subfeature": "搜索帖子", "Hours": 8},
]

# Convert to DataFrame
df = pd.DataFrame(project_structure)

# Aggregate data for visualization
module_summary = df.groupby("Module")["Hours"].sum().reset_index()

# Plotting the total estimated hours for each module
plt.figure(figsize=(10, 6))
plt.bar(module_summary["Module"], module_summary["Hours"], alpha=0.75)
plt.title("Estimated Hours by Module", fontsize=14)
plt.xlabel("Module", fontsize=12)
plt.ylabel("Estimated Hours", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()