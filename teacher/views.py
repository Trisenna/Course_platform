import token

from django.shortcuts import render
from drf_yasg import openapi

# Create your views here.
#教师发布作业
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from global_models.models import *
import os

import pandas as pd
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

#教师查看自己所交的课程
class GetCourse(APIView):
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

class GetCourseCalendar(APIView):
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
#教师登录
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
                        "message": "success"
                    }
                }
            )
        }
    )

    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')
        if account is None or password is None:
            return Response({"error": "账号或密码未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(account=account)
            if teacher.passward == password:
                return Response({"t_id": teacher.T_id})
            else:
                return Response({"error": "密码错误"}, status=status.HTTP_401_UNAUTHORIZED)
        except Teacher.DoesNotExist:
            return Response({"error": "账号不存在"}, status=status.HTTP_404_NOT_FOUND)
#教师上传课件


class UploadTeachingMaterial(APIView):


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

