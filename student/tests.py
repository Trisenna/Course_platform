from django.test import TestCase, RequestFactory, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd
from tempfile import NamedTemporaryFile

from .models import Student, StudentStudent
from .views import ImportStudent, FollowStudent
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.contrib.auth.models import User


@override_settings(MEDIA_ROOT='/tmp/')  # 使用临时目录存储上传文件
class ImportStudentTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')

    def create_csv_file(self):
        """ 创建一个简单的CSV文件 """
        data = {
            'S_id': [3, 4],
            'name': ['张三', '李四'],
            'attention_num': [0, 0],
            'account': ['zhangsan', 'lisi'],
            'password': ['password123', 'password456']
        }
        # 使用 NamedTemporaryFile 创建一个临时文件
        with NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            df = pd.DataFrame(data)
            df.to_csv(tmp.name, index=False)
            return SimpleUploadedFile('test.csv', open(tmp.name, 'rb').read())

    def test_import_student(self):
        view = ImportStudent.as_view()

        # 使用工厂创建请求
        request = self.factory.post('/student/import-student/', {'csv_file': self.create_csv_file()})
        force_authenticate(request, user=self.user)  # 模拟认证用户

        response = view(request)

        # 验证响应的状态码
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 验证响应的消息
        expected_message = '学生信息导入成功'
        actual_message = response.data.get('message', '')
        self.assertIn(expected_message, actual_message)

        # 验证数据是否正确保存到了数据库中
        from .models import Student  # 引入 Student 模型
        self.assertEqual(Student.objects.count(), 2)

        # 验证具体的学生信息是否正确保存
        student_ids = Student.objects.values_list('S_id', flat=True)
        self.assertIn(3, student_ids)
        self.assertIn(4, student_ids)
class testfollowstudent(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.student1 = Student.objects.create(S_id=1, account='zhangsan', password='password123', attention_num=0, name='张三')
        self.student2 = Student.objects.create(S_id=2, account='lisi', password='password456', attention_num=0, name='李四')


    def test_follow_student(self):
        view = FollowStudent.as_view()
        request = self.factory.post('/student/follow_student/1/2/')
        force_authenticate(request, user=self.user)
        response = view(request, s_id=1, b_id=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentStudent.objects.count(), 1)


