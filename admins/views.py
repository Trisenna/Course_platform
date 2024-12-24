from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.views.decorators.csrf import csrf_exempt
import os
import csv
from global_models.models import *
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


# 批量导入学生信息
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
                        attention_num=data.get('attention_num', None),
                        email = data.get('email'),
                        phoneNumber = data.get('phoneNumber'),
                    )
                    student.save()

                    created_students.append(student)

                    # 创建收藏夹文件夹
                    os.makedirs(f'favorite/{student.S_id}', exist_ok=True)

            return Response({"message": f"成功导入 {len(created_students)} 名学生的信息"},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# 批量导入教师信息
class ImportTeacher(APIView):

    @swagger_auto_schema(
        operation_summary='批量导入教师信息',
        operation_description="批量导入教师信息",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'csv_file': openapi.Schema(type=openapi.TYPE_FILE, description='CSV file')
            }
        ),
        responses={201: '成功导入教师信息'}
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

            teachers_data = list(reader)  # 将 CSV 数据转换为列表

            created_teachers = []
            with transaction.atomic():
                for data in teachers_data:
                    # 创建 User 实例
                    user = User.objects.create_user(
                        username=data.get('account'),
                        password=data.get('password')
                    )

                    # 创建 Teacher 实例并与 User 关联
                    teacher = Teacher(
                        T_id=data.get('T_id'),
                        user=user,
                        account=data.get('account'),
                        name=data.get('name'),
                        email=data.get('email'),
                        phoneNumber=data.get('phoneNumber'),
                    )
                    teacher.save()

                    created_teachers.append(teacher)

            return Response({"message": f"成功导入 {len(created_teachers)} 名教师的信息"},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 批量导入管理员信息
class ImportAdmin(APIView):

    @swagger_auto_schema(
        operation_summary='批量导入管理员信息',
        operation_description="批量导入管理员信息",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'csv_file': openapi.Schema(type=openapi.TYPE_FILE, description='CSV file')
            }
        ),
        responses={201: '成功导入管理员信息'}
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

            admins_data = list(reader)  # 将 CSV 数据转换为列表

            created_admins = []
            with transaction.atomic():
                for data in admins_data:
                    # 创建 User 实例
                    user = User.objects.create_user(
                        username=data.get('account'),
                        password=data.get('password')
                    )

                    # 创建 Admin 实例并与 User 关联
                    admin = Admin(
                        A_id=data.get('A_id'),
                        user=user,
                        account=data.get('account'),
                        name=data.get('name'),
                    )
                    admin.save()

                    created_admins.append(admin)

            return Response({"message": f"成功导入 {len(created_admins)} 名管理员的信息"},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 教务处发布系统通知
class PublishSystemNotice(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教务处发布系统通知',
        operation_description='教务处通过选择要发送的教师和学生发布系统通知',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='通知内容'),
                'mentionList': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户的ID'),
                            'role': openapi.Schema(type=openapi.TYPE_STRING, description='用户的角色'),
                        },
                        required=['id', 'role'],
                    ),
                    description='发送系统通知的对象数组，包含ID和角色信息，学生role为student，教师role为teacher',
                ),
            }
        ),
        responses={
            200: openapi.Response(
                '发布成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request):
        content = request.data.get('content')
        mentionList = request.data.get('mentionList')
        if mentionList is None:
            return Response({"error": "要发送系统通知的id和name未提供"}, status=status.HTTP_400_BAD_REQUEST)

        for mention in mentionList:
            information = Information.objects.create(content=content)
            user_id = mention['id']
            role = mention['role']
            # 判断系统通知要发给教师还是学生
            if role == "student":
                student = Student.objects.get(S_id=user_id)
                Releasement.objects.create(S_id=student, I_id=information, type=0)
            elif role == "teacher":
                teacher = Teacher.objects.get(T_id=user_id)
                Releasement.objects.create(T_id=teacher, I_id=information, type=0)

        return Response({"message": "success"})

# 获取所有的学生和教师
class GetAllUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获取所有的学生和教师',
        operation_description="教务处获取所有的学生和教师",
        manual_parameters=[
        ],
        responses={
            200: '成功返回所有学生和教师的id和name',
        }
    )
    def get(self, request):
        # 查询所有教师
        all_teachers = Teacher.objects.all().values('T_id', 'account', 'name', 'email', 'phoneNumber')
        # 查询所有学生
        all_students = Student.objects.all().values('S_id', 'account', 'name', 'email', 'phoneNumber')

        return Response({
            'teachers': list(all_teachers),
            'students': list(all_students)
        }, status=status.HTTP_200_OK)

# 查询所有课程
class GetAllCourses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询所有课程',
        operation_description="教务处查询所有课程",
        responses={
            200: '成功返回所有课程',
        }
    )
    def get(self, request):
        # 查询所有课程
        all_course = Course.objects.all().values()

        return Response({'courses': list(all_course),}, status=status.HTTP_200_OK)

# 创建课程
class CreateCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='创建课程',
        operation_description="教务处查询所有课程",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='课程名'),
                'introduction': openapi.Schema(type=openapi.TYPE_STRING, description='课程介绍'),
                'period': openapi.Schema(type=openapi.TYPE_INTEGER, description='时段(1-8)'),
                'credit': openapi.Schema(type=openapi.TYPE_INTEGER, description='学分'),
                'hours': openapi.Schema(type=openapi.TYPE_INTEGER, description='学时'),
                'place': openapi.Schema(type=openapi.TYPE_STRING, description='上课地点'),
            }
        ),
        responses={
            201: '成功创建课程',
        }
    )
    def post(self, request):
        name = request.data.get('name')
        introduction = request.data.get('introduction')
        period = request.data.get('period')
        credit = request.data.get('credit')
        hours = request.data.get('hours')
        place = request.data.get('place')
        print(name)
        # 创建课程
        course = Course.objects.create(name=name, introduction=introduction,
                                       period=period,credit=credit,
                                       hours=hours, place=place)

        return Response({'message': '成功创建课程'}, status=status.HTTP_201_CREATED)

# 为课程添加学生和教师
class AddCourseUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='为课程添加学生和教师',
        operation_description="根据课程id，学生id和教师id为课程添加学生和教师",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'C_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'students': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='学生的ID'
                    ),
                    description='要添加的学生的id数组',
                ),
                'teachers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='教师的ID'
                    ),
                    description='要添加的教师的id数组',
                ),
            }
        ),
        responses={
            201: '成功为课程添加学生和教师',
        }
    )
    def post(self, request):
        c_id = request.data.get('C_id')
        # 获取目标课程
        course = Course.objects.get(C_id=c_id)
        students = request.data.get('students', [])
        teachers = request.data.get('teachers', [])
        # 添加学生
        for student_id in students:
            student = Student.objects.get(S_id=student_id)
            if student is None:
                return Response({'error': 'id为' + student_id + '的学生不存在'}, status=status.HTTP_404_NOT_FOUND)
            StudentCourse.objects.create(C_id=course, S_id=student)

        # 添加教师
        for teacher_id in teachers:
            teacher = Teacher.objects.get(T_id=teacher_id)
            if teacher is None:
                return Response({'error': 'id为' + teacher_id + '的教师不存在'}, status=status.HTTP_404_NOT_FOUND)
            CourseTeacher.objects.create(C_id=course, T_id=teacher)

        return Response({'message': '成功为课程添加教师和学生'}, status=status.HTTP_201_CREATED)

# 删除课程
class DeleteCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='删除课程',
        operation_description="根据课程id删除目标课程",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'C_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            204: '成功删除课程',
        }
    )

    def delete(self, request):
        try:
            course = Course.objects.get(C_id=request.data.get('C_id'))
            course.delete()
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': '成功删除课程'}, status=status.HTTP_204_NO_CONTENT)

# 查询某个课程的所有学生
class GetCourseStudents(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询某个课程的所有学生',
        operation_description="教务处根据课程id查询该课程的所有学生",
        manual_parameters=[
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功返回该课程的所有学生',
        }
    )
    def get(self, request, c_id):
        try:
            course = Course.objects.get(C_id=c_id)
        except Course.DoesNotExist:
            c_id = str(c_id)
            return Response({"error": "id为" + c_id + "的课程不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 查询c_id课程的所有学生
        student_ids = StudentCourse.objects.filter(C_id=course).values_list('S_id', flat=True)
        all_students = Student.objects.filter(S_id__in=student_ids)
        serialized_students = [{
            'S_id': student.S_id,
            'account': student.account,
            'name': student.name,
            'email': student.email,
            'phoneNumber': student.phoneNumber,
        } for student in all_students]

        return Response({'students': serialized_students}, status=status.HTTP_200_OK)

# 查询某个课程的所有教师
class GetCourseTeachers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询某个课程的所有教师',
        operation_description="教务处根据课程id查询该课程的所有教师",
        manual_parameters=[
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功返回该课程的所有教师',
        }
    )
    def get(self, request, c_id):
        try:
            course = Course.objects.get(C_id=c_id)
        except Course.DoesNotExist:
            c_id = str(c_id)
            return Response({"error": "id为" + c_id + "的课程不存在"}, status=status.HTTP_404_NOT_FOUND)
        # 查询c_id课程的所有教师
        teacher_ids = CourseTeacher.objects.filter(C_id=course).values_list('T_id', flat=True)
        all_teachers = Teacher.objects.filter(T_id__in=teacher_ids)
        serialized_teachers = [{
            'T_id': teacher.T_id,
            'account': teacher.account,
            'name': teacher.name,
            'email': teacher.email,
            'phoneNumber': teacher.phoneNumber,
        } for teacher in all_teachers]

        return Response({'teachers': serialized_teachers, }, status=status.HTTP_200_OK)