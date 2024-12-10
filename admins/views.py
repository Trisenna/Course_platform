from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction, IntegrityError

from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
import csv

from global_models.models import Student

class ImportStudent(APIView):

    @swagger_auto_schema(
        operation_summary='批量导入学生信息',
        operation_description="批量导入学生信息",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'csv_file': openapi.Schema(type=openapi.TYPE_FILE, description='CSV file')
            }
        ),
        responses={201: '成功导入学生信息'}
    )
    # 取消csrf验证（仅用于开发或测试）
    @csrf_exempt
    def post(self, request, format=None):
        if 'csv_file' not in request.FILES:
            return Response({"error": "未找到文件"}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['csv_file']

        # 检查文件扩展名是否为 .csv
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "文件类型错误，请上传 CSV 文件"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 使用 Python 内置的 csv 模块读取文件
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            students_data = list(reader)  # 将 CSV 数据转换为列表

            created_students = []
            with transaction.atomic():
                for data in students_data:
                    # 创建 User 实例
                    user = User.objects.create_user(
                        username=data.get('account'),
                        password=data.get('password')
                    )

                    # 创建 Student 实例并与 User 关联
                    student = Student(
                        S_id=data.get('S_id'),
                        user=user,
                        account=data.get('account'),
                        name=data.get('name'),
                        attention_num=data.get('attention_num', None)
                    )
                    student.save()

                    created_students.append(student)

                    # 创建收藏夹文件夹
                    os.makedirs(f'favorite/{student.S_id}', exist_ok=True)

            return Response({"message": f"成功导入 {len(created_students)} 名学生的信息"},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
