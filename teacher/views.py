import token

from django.shortcuts import render
from drf_yasg import openapi

# Create your views here.
#教师发布作业
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from global_models.models import *
import os
import time

import pandas as pd
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q

#教师查看自己所交的课程
class GetCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师查看自己所交的课程',
        manual_parameters=[
            openapi.Parameter('t_id', openapi.IN_QUERY, '教师id', type=openapi.TYPE_INTEGER),
        ]
    )

    def get(self, request,t_id):


        teacher = Teacher.objects.get(T_id=t_id)


        course_id = CourseTeacher.objects.filter(T_id=teacher).values('C_id')
        course = Course.objects.filter(C_id__in=course_id)
        course_list = []
        for c in course:
            #添加课程信息
            course_list.append({
                'C_id':c.C_id,
                'name':c.name,
                'period':c.period,
            })
        return Response({'course_list':course_list})

#教师查看自己所交的课程的学生
class GetCourseStudent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师查看自己所交的课程的学生',
        operation_description='允许教师通过课程名称和学期来获取该课程的学生列表。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'C_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),

            }
        ),
        responses={
            200: openapi.Response(
                '返回学生列表',
                examples={
                    "application/json": {
                        "student_list": [
                            {
                                "S_id": "1",
                                "name": "张三"
                            },
                            {
                                "S_id": "2",
                                "name": "李四"
                            }
                        ]
                    }
                }
            )
        }
    )

    def  post(self, request,t_id):
        teacher = Teacher.objects.get(T_id=t_id)
        C_id = request.data.get('C_id')





        course = Course.objects.filter(C_id=C_id)


        student_list = []
        for c in course:
            student_id = StudentCourse.objects.filter(C_id=c).values('S_id')
            student = Student.objects.filter(S_id__in=student_id)
            for s in student:
                #添加学生信息
                student_list.append({
                    'S_id':s.S_id,
                    'name':s.name,

                })
        return Response({'student_list':student_list})

#教师修改某个课程的课程介绍，post
class AdjustCourseInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师修改某个课程的课程介绍',
        operation_description='允许教师通过课程id来修改该课程的课程介绍。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'introduction': openapi.Schema(type=openapi.TYPE_STRING, description='课程介绍'),

            }
        ),
        responses={
            200: openapi.Response(
                '修改成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request,t_id):
        c_id = request.data.get('c_id')
        introduction = request.data.get('introduction')
        course = Course.objects.get(C_id=c_id)
        course.introduction = introduction
        course.save()
        return Response({'message':'success'})
#教师修改某个课程的课程大纲，大纲为一个文件，post
class AdjustCourseOutline(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师修改某个课程的课程大纲',
        operation_description='允许教师通过课程id来修改该课程的课程大纲。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'Syllabus': openapi.Schema(type=openapi.TYPE_FILE, description='大纲'),

            }
        ),
        responses={
            200: openapi.Response(
                '修改成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request,t_id):
        c_id = request.data.get('c_id')
        Syllabus = request.FILES.get('Syllabus')
        course = Course.objects.get(C_id=c_id)
        course.Syllabus = Syllabus
        course.save()
        return Response({'message':'success'})
#教师上传教学日历
class AdjustCourseCalendar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师修改教学日历',
        operation_description='允许教师通过课程id来上传该课程的教学日历。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'calendar': openapi.Schema(type=openapi.TYPE_FILE, description='教学日历'),

            }
        ),
        responses={
            200: openapi.Response(
                '上传成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request,t_id):
        c_id = request.data.get('c_id')
        calendar = request.FILES.get('calendar')
        course = Course.objects.get(C_id=c_id)
        course.calendar = calendar
        course.save()
        return Response({'message':'success'})
from django.http import FileResponse
# 获取课程教学日历
class GetCourseCalendar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看教学日历',
        operation_description='允许教师通过课程id来查看该课程的教学日历。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回教学日历',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/calendar.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            # 假设calendar字段保存的是文件路径
            file_path = course.calendar.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

#查看课程大纲
class GetCourseOutline(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看课程大纲',
        operation_description='允许教师通过课程id来查看该课程的课程大纲。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回课程大纲',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/syllabus.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            # 假设Syllabus字段保存的是文件路径
            file_path = course.Syllabus.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#查看课程介绍
class GetCourseIntroduction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看课程介绍',
        operation_description='允许教师通过课程id来查看该课程的课程介绍。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回课程介绍',
                examples={
                    "application/json": {
                        "introduction": "这是一个课程介绍"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            return Response({"introduction": course.introduction})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师发布课程通知
class PublishNotice(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师发布课程通知',
        operation_description='允许教师通过课程id来发布课程通知。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='通知内容'),
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

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        content = request.data.get('content')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            teacher = Teacher.objects.get(T_id=t_id)
            # 根据通知内容创建通知
            information = Information.objects.create(content=content)
            information.save()
            #查询课程的学生
            student = StudentCourse.objects.filter(C_id=course)
            for s in student:
                #将通知发送给学生
                Releasement.objects.create(S_id=s.S_id, I_id=information, type=1, C_id=course, T_id=teacher)


            return Response({"message": "success"})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

class ValidateTeacherLogin(APIView):

    @swagger_auto_schema(
        operation_summary='教师登录',
        operation_description='允许教师通过账号和密码登录。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account': openapi.Schema(type=openapi.TYPE_STRING, description='账号'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            }
        ),
        responses={
            200: openapi.Response(
                '登录成功',
                examples={
                    "application/json": {
                        "message": "success",
                        "t_id": 1,
                        "token": "your-token-value"
                    }
                }
            ),
            400: '账号或密码未提供',
            401: '密码错误',
            404: '账号不存在'
        }
    )
    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        if account is None or password is None:
            return Response({"error": "账号或密码未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(account=account)
            if check_password(password, teacher.password):
                token, created = Token.objects.get_or_create(user=teacher)
                return Response({
                    "message": "success",
                    "t_id": teacher.T_id,
                    "token": token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "密码错误"}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({"error": "账号不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师上传课件
class UploadTeachingMaterial(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_summary="教师上传课件",
        operation_description="教师上传课件",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),

        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='课件文件'),
            }
        ),
        responses={201: '课件上传成功'}
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        file = request.data.get('file')
        if not file:
            return Response({"error": "文件未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            resource = Resource(file=file, type='0')  # 0 表示课件
            resource.save()

            # 将资源关联到课程
            course_resource = CourseResource(R_id=resource, C_id=course)
            course_resource.save()

            return Response({'message': '文件上传成功'}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师上传试题
class UploadTest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师上传试题',
        operation_description='允许教师通过课程id来上传试题。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='试题文件'),
            }
        ),
        responses={
            200: openapi.Response(
                '上传成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        file = request.data.get('file')
        if not file:
            return Response({"error": "文件未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            resource = Resource(file=file, type='1')  # 1 表示试题
            resource.save()

            # 将资源关联到课程
            course_resource = CourseResource(R_id=resource, C_id=course)
            course_resource.save()

            return Response({'message': 'success'})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师上传习题
class UploadExercise(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师上传习题',
        operation_description='允许教师通过课程id来上传习题。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='习题文件'),
            }
        ),
        responses={
            200: openapi.Response(
                '上传成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        file = request.data.get('file')
        if not file:
            return Response({"error": "文件未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            resource = Resource(file=file, type='2')  # 2 表示习题
            resource.save()

            # 将资源关联到课程
            course_resource = CourseResource(R_id=resource, C_id=course)
            course_resource.save()

            return Response({'message': 'success'})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师查看课件
class GetCourseMaterial(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看课件',
        operation_description='允许教师通过课程id来查看该课程的课件。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回课件',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/material.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            # 获取课程的课件资源
            resource = CourseResource.objects.filter(C_id=course, R_id__type='0').first()
            if resource is None:
                return Response({"error": "课件不存在"}, status=status.HTTP_404_NOT_FOUND)

            # 假设file字段保存的是文件路径
            file_path = resource.R_id.file.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师查看试题
class GetTest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看试题',
        operation_description='允许教师通过课程id来查看该课程的试题。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回试题',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/test.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            # 获取课程的试题资源
            resource = CourseResource.objects.filter(C_id=course, R_id__type='1').first()
            if resource is None:
                return Response({"error": "试题不存在"}, status=status.HTTP_404_NOT_FOUND)

            # 假设file字段保存的是文件路径
            file_path = resource.R_id.file.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

#教师查看习题
class GetExercise(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看习题',
        operation_description='允许教师通过课程id来查看该课程的习题。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回习题',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/exercise.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            # 获取课程的习题资源
            resource = CourseResource.objects.filter(C_id=course, R_id__type='2').first()
            if resource is None:
                return Response({"error": "习题不存在"}, status=status.HTTP_404_NOT_FOUND)

            # 假设file字段保存的是文件路径
            file_path = resource.R_id.file.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师上传某个课程作业
class UploadWork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师上传作业',
        operation_description='允许教师通过课程id来上传作业，并将其分配给该课程的所有学生。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
                'content': openapi.Schema(type=openapi.TYPE_FILE, description='作业内容文件'),
                'start': openapi.Schema(type=openapi.FORMAT_DATE, description='开始日期'),
                'end': openapi.Schema(type=openapi.FORMAT_DATE, description='截止日期'),

                'title': openapi.Schema(type=openapi.TYPE_STRING, description='作业标题'),
            }
        ),
        responses={
            201: openapi.Response(
                '作业上传成功',
                examples={
                    "application/json": {
                        "message": "作业已成功上传并分配给学生。",
                        "work_id": 123
                    }
                }
            )
        }
    )
    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        content = request.FILES.get('content')
        start = request.data.get('start')
        end = request.data.get('end')

        if c_id is None or content is None or start is None or end is None:
            return Response({"error": "缺少必要的参数"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(T_id=t_id)
            course = Course.objects.get(C_id=c_id)

            # 创建作业
            work = Work.objects.create(
                content=content,
                start=start,
                end=end,
                title=request.data.get('title'),
            )

            # 获取课程中的所有学生
            students_in_course = StudentCourse.objects.filter(C_id=course).values_list('S_id', flat=True)

            for student in students_in_course:
                student_obj = Student.objects.get(S_id=student)
                # 创建学生作业记录
                DoWork.objects.create(
                    S_id=student_obj,
                    W_id=work,
                    C_id=course,
                    T_id=teacher,
                    is_push=False,
                    file=None  # 学生尚未提交作业
                )

            return Response({"message": "作业已成功上传并分配给学生。", "work_id": work.W_id},
                            status=status.HTTP_201_CREATED)

        except Teacher.DoesNotExist:
            return Response({"error": "教师不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师查看自己发布的作业
class GetWork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师查看自己发布的作业',
        operation_description='允许教师通过课程id来查看该课程的作业。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回作业列表',
                examples={
                    "application/json": {
                        "work_list": [
                            {
                                "W_id": 1,
                                "title": "作业标题",
                                "start": "2021-01-01",
                                "end": "2021-01-10"
                            }
                        ]
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            teacher = Teacher.objects.get(T_id=t_id)
            w=DoWork.objects.filter(C_id=course, T_id=teacher).values('W_id').distinct()

            work_list = []
            for work in w:
                work = Work.objects.get(W_id=work['W_id'])


                work_list.append({
                    'W_id': work.W_id,
                    'title': work.title,
                    'start': work.start,
                    'end': work.end
                })

            return Response({"work_list": work_list})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

#教师查看某个作业的提交情况
class GetWorkSubmission(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师查看某个作业的提交情况',
        operation_description='允许教师通过作业id来查看该作业的提交情况。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'w_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='作业id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回提交情况',
                examples={
                    "application/json": {
                        "submission_list": [
                            {
                                "S_id": 1,
                                "name": "张三",
                                "is_push": True,
                                "file": "http://example.com/download/path/to/file"
                            }
                        ]
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        w_id = request.data.get('w_id')
        if w_id is None:
            return Response({"error": "作业id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(T_id=t_id)
            work = Work.objects.get(W_id=w_id)

            # 获取作业的提交情况
            submission_list = []
            submissions = DoWork.objects.filter(W_id=work, T_id=teacher)
            for submission in submissions:
                student = Student.objects.get(S_id=submission.S_id.S_id)
                submission_list.append({
                    'S_id': student.S_id,
                    'name': student.name,
                    'is_push': submission.is_push,
                    'file': submission.file.url if submission.file else None
                })

            return Response({"submission_list": submission_list})
        except Teacher.DoesNotExist:
            return Response({"error": "教师不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Work.DoesNotExist:
            return Response({"error": "作业不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师查看学生作业
class GetStudentWork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师查看学生作业',
        operation_description='允许教师通过作业id和学生id来查看学生提交的作业。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'w_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='作业id'),
                's_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='学生id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回学生作业',
                examples={
                    "application/json": {
                        "file": "http://example.com/download/path/to/file"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        w_id = request.data.get('w_id')
        s_id = request.data.get('s_id')
        if w_id is None or s_id is None:
            return Response({"error": "缺少必要的参数"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(T_id=t_id)
            work = Work.objects.get(W_id=w_id)
            student = Student.objects.get(S_id=s_id)

            # 获取学生提交的作业
            submission = DoWork.objects.get(W_id=work, S_id=student)
            #以文件流的形式返回文件
            response = FileResponse(open(submission.file.path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(submission.file.path)}"'
            return response



        except Teacher.DoesNotExist:
            return Response({"error": "教师不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Work.DoesNotExist:
            return Response({"error": "作业不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)
        except DoWork.DoesNotExist:
            return Response({"error": "学生未提交作业"}, status=status.HTTP_404_NOT_FOUND)
#教师批改作业
class CorrectWork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师批改作业',
        operation_description='允许教师通过作业id和学生id来批改作业。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'w_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='作业id'),
                's_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='学生id'),
                'score': openapi.Schema(type=openapi.TYPE_INTEGER, description='分数'),
            }
        ),
        responses={
            200: openapi.Response(
                '批改成功',
                examples={
                    "application/json": {
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request, t_id):
        w_id = request.data.get('w_id')
        s_id = request.data.get('s_id')
        score = request.data.get('score')
        if w_id is None or s_id is None or score is None:
            return Response({"error": "缺少必要的参数"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(T_id=t_id)
            work = Work.objects.get(W_id=w_id)
            student = Student.objects.get(S_id=s_id)

            # 获取学生提交的作业
            submission = DoWork.objects.get(W_id=work, S_id=student)

            # 更新作业分数
            submission.score = score
            submission.save()

            return Response({"message": "success"})
        except Teacher.DoesNotExist:
            return Response({"error": "教师不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Work.DoesNotExist:
            return Response({"error": "作业不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "学生不存在"}, status=status.HTTP_404_NOT_FOUND)
        except DoWork.DoesNotExist:
            return Response({"error": "学生未提��作业"}, status=status.HTTP_404_NOT_FOUND)



# 教师查询个人信息
class GetTeacherInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师查询个人信息',
        operation_description="教师查询个人信息",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: '返回个人信息'}
    )

    def get(self, request, t_id):
        teacher = get_object_or_404(Teacher, pk=t_id)
        return Response({'teacher': {'account': teacher.account, 'name': teacher.name,
                                     'phoneNumber': teacher.phoneNumber, 'email': teacher.email}}, status=status.HTTP_200_OK)

# 教师修改个人信息
class AdjustTeacherInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师修改个人信息',
        operation_description="教师修改邮箱或手机号",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='新邮箱'),
                'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING, description='新手机号')
            }
        ),
        responses={200: '成功更新个人信息'}
    )

    def post(self, request, t_id):
        teahcer = get_object_or_404(Teacher, pk=t_id)
        email = request.data.get('email')
        phoneNumber = request.data.get('phoneNumber')

        if email:
            teahcer.email = email

        if phoneNumber:
            teahcer.phoneNumber = phoneNumber

        teahcer.save()
        return Response({'status': 'success', 'message': 'Personal info updated successfully.'},
                        status=status.HTTP_200_OK)

# 用户发布帖子到课程下的评论区
class CreateDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户发布帖子到课程评论区',
        operation_description="用户根据课程ID发布帖子，包含标题和内容",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='帖子标题'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='帖子内容'),
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
                    description='被@用户的对象数组，包含ID和角色信息，学生role为student，教师role为teacher',
                ),
            },
        ),
        responses={
            201: '成功创建帖子',
        }
    )

    def post(self, request, t_id, c_id):
        title = request.data.get('title')
        content = request.data.get('content')
        teacher = Teacher.objects.get(T_id=t_id)
        #创建帖子
        discuss = Discuss(title=title, content=content, T_id=teacher)
        discuss.save()
        #创建帖子和课程的联系
        c = Course.objects.get(C_id=c_id)
        discou = DisCou(C_id=c, D_id=discuss)
        discou.save()

        # 检查是否@其他用户
        mentionList = request.data.get('mentionList', [])
        if mentionList:
            for mention in mentionList:
                send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                information = Information.objects.create(content=(send_time + " 课程：" + c.name + " 有人@了你，请点击查看"))
                id = mention['id']
                role = mention['role']
                course = Course.objects.get(C_id=c_id)
                # 判断被@的用户是教师还是学生
                if role == "student":
                    student = Student.objects.get(S_id=id)
                    Releasement.objects.create(S_id=student, I_id=information, type=1, C_id=course)
                elif role == "teacher":
                    teacher = Teacher.objects.get(T_id=id)
                    Releasement.objects.create(T_id=teacher, I_id=information, type=1, C_id=course)

        return Response({'message': 'Successfully created discuss.'}, status=status.HTTP_201_CREATED)

# 查看课程的讨论区
class GetDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询此课程讨论区的所有帖子',
        operation_description="根据课程ID查询此课程讨论区的所有帖子",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '返回帖子列表',
        }
    )

    def get(self, request, t_id, c_id):
        # 查询此课程讨论区的所有帖子
        discous = DisCou.objects.filter(C_id=c_id)
        all_discuss_ids = [discou.D_id.D_id for discou in discous]
        all_discuss = Discuss.objects.filter(D_id__in=all_discuss_ids).values()

        return Response({'all_discuss': list(all_discuss)}, status=status.HTTP_200_OK)

# 用户在帖子下发表评论
class CreateReply(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户在帖子下发表评论',
        operation_description="用户在帖子下发表评论",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'answer': openapi.Schema(type=openapi.TYPE_STRING, description='用户的评论内容'),
            },
        ),
        responses={
            201: '成功评论帖子',
        }
    )

    def post(self, request, t_id, d_id):
        answer = request.data.get('answer')
        teacher = Teacher.objects.get(T_id=t_id)
        #用户评论帖子
        reply = Reply(answer=answer, T_id=teacher)
        reply.save()
        #创建帖子和评论的联系
        discuss = Discuss.objects.get(D_id=d_id)
        disreply = DiscussReply(R_id=reply, D_id=discuss)
        disreply.save()
        return Response({'message': 'Successfully created reply.'}, status=status.HTTP_201_CREATED)

# 查看帖子的评论
class GetReply(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询此帖子的所有评论',
        operation_description="根据帖子ID查询此帖子的所有评论",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '返回评论列表',
        }
    )

    def get(self, request, t_id, d_id):
        # 查询此帖子的所有评论
        disreplys = DiscussReply.objects.filter(D_id=d_id)
        all_replys_id = [disreply.R_id.R_id for disreply in disreplys]
        all_replys = Reply.objects.filter(R_id__in=all_replys_id).values()

        return Response({'all_replies': list(all_replys)}, status=status.HTTP_200_OK)

# 用户点赞帖子
class LikeDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户点赞帖子',
        operation_description="根据帖子ID点赞帖子",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功点赞帖子',
        }
    )

    def post(self, request, t_id, d_id):
        # 帖子的点赞数+1
        discuss = Discuss.objects.get(D_id=d_id)
        discuss.likes = discuss.likes+1
        discuss.save()

        return Response({'message': 'Successfully liked discuss.'}, status=status.HTTP_200_OK)

# 用户取消点赞帖子
class CancelLikeDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户取消点赞帖子',
        operation_description="根据帖子ID取消点赞帖子",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功取消点赞帖子',
        }
    )

    def post(self, request, t_id, d_id):
        # 帖子的点赞数-1
        discuss = Discuss.objects.get(D_id=d_id)
        discuss.likes = discuss.likes-1
        discuss.save()

        return Response({'message': 'Successfully cancel liked discuss.'}, status=status.HTTP_200_OK)

# 用户点赞帖子的评论
class LikeDiscussReply(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户点赞帖子的评论',
        operation_description="根据帖子ID点赞帖子的评论",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'r_id',
                openapi.IN_PATH,
                description='帖子评论ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功点赞帖子的评论',
        }
    )

    def post(self, request, t_id, d_id, r_id):
        # 帖子某个评论的点赞数+1
        reply = Reply.objects.get(R_id=r_id)
        reply.likes = reply.likes+1
        reply.save()

        return Response({'message': 'Successfully liked discuss reply.'}, status=status.HTTP_200_OK)

# 用户取消点赞帖子的评论
class CancelLikeDiscussReply(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户取消点赞帖子的评论',
        operation_description="根据帖子评论ID取消点赞帖子的评论",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'r_id',
                openapi.IN_PATH,
                description='帖子评论ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功点赞帖子的评论',
        }
    )

    def post(self, request, t_id, d_id, r_id):
        # 帖子某个评论的点赞数-1
        reply = Reply.objects.get(R_id=r_id)
        reply.likes = reply.likes-1
        reply.save()

        return Response({'message': 'Successfully cancel liked discuss reply.'}, status=status.HTTP_200_OK)

# 查询帖子的点赞数
class GetLikesOfDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获取帖子的点赞数',
        operation_description="根据帖子ID获取帖子的点赞数",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功返回帖子的点赞数',
        }
    )

    def get(self, request, t_id, d_id):
        discuss = Discuss.objects.get(D_id=d_id)

        return Response({'discuss_likes': discuss.likes}, status=status.HTTP_200_OK)

# 查询帖子评论的点赞数
class GetLikesOfReply(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获取帖子的评论的点赞数',
        operation_description="根据评论ID获取点赞数",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'r_id',
                openapi.IN_PATH,
                description='评论ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功帖子的评论的点赞数',
        }
    )

    def get(self, request, t_id, d_id, r_id):
        reply = Reply.objects.get(R_id=r_id)

        return Response({'reply_likes': reply.likes}, status=status.HTTP_200_OK)

# 教师可以删除讨论区的帖子
class DeleteDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师删除讨论区的帖子',
        operation_description="根据帖子ID删除帖子",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            204: '成功删除帖子',
            400: '删除失败'
        }
    )

    def post(self, request, t_id, d_id):
        # 删除指定帖子
        try:
            discuss = Discuss.objects.get(D_id=d_id)
            discuss.delete()
            return Response({'message': 'Successfully deleted discuss.'}, status=status.HTTP_204_NO_CONTENT)
        except Discuss.DoesNotExist:
            return Response({'message': 'unSuccessfully deleted discuss.'}, status=status.HTTP_400_BAD_REQUEST)

# 教师可以删除帖子的评论
class DeleteReply(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='教师删除帖子的评论',
        operation_description="根据评论ID删除帖子评论",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'r_id',
                openapi.IN_PATH,
                description='帖子评论ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功删除帖子的评论',
        }
    )
    def post(self, request, t_id, d_id, r_id):
        # 删除帖子的某条评论
        reply = Reply.objects.get(R_id=r_id)
        reply.delete()

        return Response({'message': 'Successfully deleted discuss_reply.'}, status=status.HTTP_200_OK)

# 用户通过关键词模糊搜索帖子和评论
class SearchContent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户通过关键词模糊搜索帖子和评论的内容',
        operation_description="用户通过关键词模糊搜索帖子和评论的内容，包含标题和内容",
        manual_parameters=[
            openapi.Parameter(
                'keyword',
                openapi.IN_QUERY,
                description='关键词',
                required=True,
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: '成功搜索含有关键词的帖子和评论',
        }
    )

    def get(self, request, t_id):
        keyword = request.query_params.get('keyword', '').strip()
        if not keyword:
            return Response({'message': 'Keyword is required for searching.'}, status=status.HTTP_400_BAD_REQUEST)

        # 在Discuss和Reply中模糊搜索
        discuss_results = Discuss.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        )
        reply_results = Reply.objects.filter(
            Q(answer__icontains=keyword)
        )

        # 序列化搜索结果
        results = {
            'discusses': [
                {'D_id': d.D_id, 'title': d.title, 'content': d.content, 'likes': d.likes}
                for d in discuss_results
            ],
            'replies': [
                {'R_id': r.R_id, 'answer': r.answer, 'likes': r.likes}
                for r in reply_results
            ],
        }

        return Response(results, status=status.HTTP_200_OK)

# 获取某课程的所有教师和学生
class GetList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获取某课程的所有教师和学生',
        operation_description="用户输入@后给用户返回此课程的所有教师和学生",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功返回此课程的所有学生和教师的id和name',
        }
    )

    def get(self, request, t_id, c_id):
        # 查询课程的教师
        teachers = CourseTeacher.objects.filter(C_id=c_id).exclude(T_id=t_id)
        all_teachers_ids = [teacher.T_id.T_id for teacher in teachers]
        all_teachers = Teacher.objects.filter(T_id__in=all_teachers_ids).values('T_id', 'name')
        # 查询课程的所有学生
        student_courses = StudentCourse.objects.filter(C_id=c_id)
        all_students_ids = [student_course.S_id.S_id for student_course in student_courses]
        all_students = Student.objects.filter(S_id__in=all_students_ids).values('S_id', 'name')

        return Response({
            'teachers': list(all_teachers),
            'students': list(all_students)
        }, status=status.HTTP_200_OK)

# 查询某个教师在课程讨论区被@的通知
class MyCourseNotice(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询某个教师的所有课程通知(包括该用户在课程讨论区被@的通知)',
        operation_description="查询某个教师的所有课程通知的C_id和对应的I_id,type=1",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],

        responses={200: '返回教师的课程通知列表'}
    )

    def get(self, request, t_id):
        # 查询被@的通知
        notices = Releasement.objects.filter(S_id__isnull=True, T_id=t_id, type=1).values('C_id', 'I_id')
        #根据C_id查到课程名，根据I_id查到通知内容
        for notice in notices:
            course = Course.objects.filter(C_id=notice['C_id']).values('name').first()
            information = Information.objects.filter(I_id=notice['I_id']).values('content').first()
            notice['course'] = course
            notice['information'] = information


        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)

# 查询某个教师的所有系统通知
class MySystemNotice(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary= '查询某个教师的所有系统通知',
        operation_description="查询某个教师的所有系统通知的I_id",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],

        responses={200: '返回教师的系统通知列表'}
    )

    def get(self, request, t_id):
        exists_teacher = Teacher.objects.filter(T_id=t_id).exists()
        if not exists_teacher:
            return Response({"error": "该教师不存在"}, status=status.HTTP_404_NOT_FOUND)
        exists_releasement = Releasement.objects.filter(T_id=t_id, type=0).exists()
        print(exists_releasement)
        if not exists_releasement:
            return Response({"error": "该教师没有系统通知"}, status=status.HTTP_404_NOT_FOUND)
        notices = Releasement.objects.filter(T_id=t_id, type=0).values('I_id')
        #根据I_id查到通知内容
        for notice in notices:
            information = Information.objects.filter(I_id=notice['I_id']).values('content').first()
            notice['information'] = information
        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)

# 处理用户发布帖子的关键词
class DiscussKeyword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='处理用户发布帖子的关键词',
        operation_description="处理用户发布帖子的关键词，建立其与帖子的联系",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'd_id',
                openapi.IN_PATH,
                description='帖子ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'keyWordList': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='关键词的内容',
                    ),
                    description='讨论贴的关键词'
                ),

            },
        ),
        responses={
            201: '成功创建帖子',
        }
    )
    def post(self, request, t_id, d_id):
        keyWordList = request.data.get('keyWordList')
        # 检查用户是否#关键词
        if keyWordList:
            # 建立每一个关键词与它所属帖子的联系
            for content in keyWordList:
                print(content)
                keyword = KeyWord.objects.create(content=content)
                discuss = Discuss.objects.get(D_id=d_id)
                keyword_discuss = KeyWordDiscuss.objects.create(D_id=discuss, K_id=keyword)

        return Response({'message': 'Successfully created discuss.'}, status=status.HTTP_201_CREATED)

# 获取某课程讨论区的所有话题关键词
class GetKeyWords(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获取某课程讨论区的所有话题关键词',
        operation_description="获取某课程讨论区的所有话题关键词",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功返回此课程的所有话题关键词',
        }
    )
    def get(self, request, t_id, c_id):
        # 查询c_id课程的所有帖子
        discuss_s = DisCou.objects.filter(C_id=c_id).select_related('D_id')
        # 获取与这些讨论帖相关的所有关键词ID
        keyword_ids = KeyWordDiscuss.objects.filter(D_id__in=[d.D_id for d in discuss_s]).values_list('K_id',)
        # 获取所有关联的关键词
        keywords = KeyWord.objects.filter(K_id__in=keyword_ids).values('K_id', 'content')

        return Response({'keywords': list(keywords)}, status=status.HTTP_200_OK)

# 获取此课程讨论区含有目标关键词的所有帖子
class GetALLTargetDiscuss(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获取此课程讨论区含有目标关键词的所有帖子',
        operation_description="获取c_id课程讨论区含有k_id关键词的所有帖子",
        manual_parameters=[
            openapi.Parameter(
                't_id',
                openapi.IN_PATH,
                description='教师ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'k_id',
                openapi.IN_PATH,
                description='关键词ID',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: '成功返回此课程含有目标关键词的所有帖子',
        }
    )
    def get(self, request, t_id, c_id, k_id):
        # 查询c_id课程的所有帖子
        discuss_ids = DisCou.objects.filter(C_id=c_id).values_list('D_id', flat=True)
        # 查询这些帖子中含有目标关键词的帖子ID
        target_discuss_ids = KeyWordDiscuss.objects.filter(D_id__in=discuss_ids, K_id=k_id).values_list('D_id',
                                                                                                        flat=True)
        # 获取帖子详情
        discusses = Discuss.objects.filter(D_id__in=target_discuss_ids).values()

        return Response({'discusses': list(discusses)}, status=status.HTTP_200_OK)