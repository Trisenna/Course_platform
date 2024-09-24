import pandas as pd
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema


from .models import *



# 查询某个学生的所有课程的name, C_id
class MyCourseList(APIView):
    @swagger_auto_schema(
        operation_description="查询某个学生的所有课程的name,C_id",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='学生id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],

        responses={200: '返回学生的课程列表'}
    )

    def get(self, request, s_id):
        courses = Course.objects.filter(C_id__in=StudentCourse.objects.filter(S_id=s_id).values('C_id'))
        course_names = list(courses.values('name', 'C_id'))
        return Response({'courses': course_names}, status=status.HTTP_200_OK)





# 查询某个学生的所有课程通知
class MyCourseNotice(APIView):
    @swagger_auto_schema(
        operation_description="查询某个学生的所有课程通知的C_id和对应的I_id",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='学生id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],

        responses={200: '返回学生的课程通知列表'}
    )

    def get(self, request, s_id):
        notices = Releasement.objects.filter(S_id=s_id, type=1).values('C_id', 'I_id')
        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)


# 根据课程id查询课程名称
class GetCourseName(APIView):
    @swagger_auto_schema(
        operation_description="根据课程id查询课程名称",
        manual_parameters=[
            openapi.Parameter(
                'c_id',
                openapi.IN_PATH,
                description='课程id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],

        responses={200: '返回课程名称'}
    )

    def get(self, request, c_id):
        course = Course.objects.filter(C_id=c_id).values('name').first()
        if course:
            return Response({'course': course}, status=status.HTTP_200_OK)
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


# 根据通知id查询通知内容
class GetInformationContent(APIView):
    @swagger_auto_schema(
        operation_description="根据通知id查询通知内容",
        manual_parameters=[
            openapi.Parameter(
                'i_id',
                openapi.IN_PATH,
                description='通知id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],


        responses={200: '返回通知内容'}
    )


    def get(self, request, i_id):
        info = Information.objects.filter(I_id=i_id).values('content').first()
        if info:
            return Response({'information': info}, status=status.HTTP_200_OK)
        return Response({'error': 'Information not found'}, status=status.HTTP_404_NOT_FOUND)


# 查询某个学生的所有系统通知
class MySystemNotice(APIView):
    @swagger_auto_schema(
        operation_description="查询某个学生的所有系统通知的I_id",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='学生id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],

        responses={200: '返回学生的系统通知列表'}
    )

    def get(self, request, s_id):
        notices = Releasement.objects.filter(S_id=s_id, type=0).values('I_id')
        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)

#
# # 查询其他学生的所有收藏夹
# class GetFavoriteName(APIView):
#     @swagger_auto_schema(
#         operation_description="查询其他学生的所有收藏夹",
#         manual_parameters=[
#             openapi.Parameter(
#                 's_id',
#                 openapi.IN_PATH,
#                 description='查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#             openapi.Parameter(
#                 'b_id',
#                 openapi.IN_PATH,
#                 description='被查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#         ],
#
#         responses={200: '返回被查询者的所有收藏夹'}
#     )
#
#
#     def get(self, request, s_id, b_id):
#         if s_id == b_id:
#             fav = Note.objects.filter(S_id=b_id).values('favoritename').distinct()
#         else:
#             fav = Note.objects.filter(S_id=b_id, type=1).values('favoritename').distinct()
#         return Response({'favoritename': list(fav)}, status=status.HTTP_200_OK)
#
#
# # 获得一个收藏夹的所有笔记
# class GetNoteByFavoriteName(APIView):
#     @swagger_auto_schema(
#         operation_description="获得一个收藏夹的所有笔记, s_id为查询者id，b_id为被查询者id,如果查询者和被查询者是同一个人，返回所有笔记，否则只返回可见笔记",
#         manual_parameters=[
#             openapi.Parameter(
#                 's_id',
#                 openapi.IN_PATH,
#                 description='查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#             openapi.Parameter(
#                 'b_id',
#                 openapi.IN_PATH,
#                 description='被查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#             openapi.Parameter(
#                 'favoritename',
#                 openapi.IN_PATH,
#                 description='收藏夹名',
#                 required=True,
#                 type=openapi.TYPE_STRING,
#             ),
#         ],
#         responses={200: '返回被查询者的收藏夹的所有笔记'}
#     )
#
#     def get(self, request, s_id, b_id, favoritename):
#         if s_id == b_id:
#             #type!=2
#             notes = Note.objects.filter(S_id=b_id, favoritename=favoritename).exclude(type=2)
#         else:
#             notes = Note.objects.filter(S_id=b_id, favoritename=favoritename, type=1)
#         return Response({'notes': list(notes.values('N_id', 'addr'))}, status=status.HTTP_200_OK)
#
# #用户创建收藏夹
# class CreateFavorite(APIView):
#     @swagger_auto_schema(
#         operation_description="用户创建收藏夹",
#         manual_parameters=[
#             openapi.Parameter(
#                 's_id',
#                 openapi.IN_PATH,
#                 description='用户id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#         ],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'favoritename': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名'),
#                 'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='保存后是否可见'),
#             }
#         ),
#         responses={201: '成功创建收藏夹', 400: 'Favorite name already exists.'}
#
#     )
#
#     def post(self, request, s_id):
#         favoritename = request.data.get('favoritename')
#         visible = request.data.get('type')
#         #查询note中所有s_id为s_id的数据
#         notes = Note.objects.filter(S_id=s_id).values('favoritename')
#         #判断是否有重名的收藏夹
#         for note in notes:
#             if note['favoritename'] == request.data.get('favoritename'):
#                 return Response({'error': 'Favorite name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
#         s=Student.objects.get(S_id=s_id)
#         f=FavoriteISopen(S_id=s,name=favoritename,is_public=visible)
#
#
#         new_note = Note(
#             S_id=s_id,
#             favoritename=favoritename,
#             like_num=0,
#             follow_num=0,
#             type=2,
#         )
#         new_note.save()
#         return Response({'message': 'Successfully created favorite.'}, status=status.HTTP_201_CREATED)
# # 用户收藏笔记
# class FavNote(APIView):
#     @swagger_auto_schema(
#         operation_description="用户收藏笔记",
#         manual_parameters=[
#             openapi.Parameter(
#                 's_id',
#                 openapi.IN_PATH,
#                 description='查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#             openapi.Parameter(
#                 'b_id',
#                 openapi.IN_PATH,
#                 description='被查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#         ],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'favoritename': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名'),
#                 'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='保存后是否可见'),
#                 'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='笔记id')
#             }
#         ),
#         responses={201: '成功收藏笔记'}
#     )
#
#     def post(self, request, s_id, b_id):
#         favoritename = request.data.get('favoritename')
#         visible = request.data.get('type')
#         note_id = request.data.get('note_id')
#
#         note = get_object_or_404(Note, N_id=note_id, S_id=b_id)
#         note.follow_num += 1
#         note.save()
#
#         new_note = Note(
#
#             S_id=s_id,
#             favoritename=favoritename,
#             like_num=0,
#             follow_num=0,
#             type=visible,
#             addr=note.addr
#         )
#         new_note.save()
#         print(new_note)
#
#         return Response({'message': 'Successfully liked note.'}, status=status.HTTP_201_CREATED)
#
#
# # 用户取消收藏笔记
# class UnfavNote(APIView):
#     @swagger_auto_schema(
#         operation_description="用户取消收藏笔记",
#         manual_parameters=[
#             openapi.Parameter(
#                 's_id',
#                 openapi.IN_PATH,
#                 description='查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#             openapi.Parameter(
#                 'b_id',
#                 openapi.IN_PATH,
#                 description='被查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#         ],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='笔记id')
#             }
#         ),
#         responses={200: '成功取消收藏笔记'}
#     )
#
#     def post(self, request, s_id, b_id):
#         note_id = request.data.get('note_id')
#         note = get_object_or_404(Note, N_id=note_id, S_id=b_id)
#         note.fllow_num -= 1
#         note.save()
#         return Response({'message': 'Successfully unliked note.'}, status=status.HTTP_200_OK)
#
#
# # 用户点赞笔记
# class LikeNote(APIView):
#     @swagger_auto_schema(
#         operation_description="用户点赞笔记",
#         manual_parameters=[
#             openapi.Parameter(
#                 's_id',
#                 openapi.IN_PATH,
#                 description='查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#             openapi.Parameter(
#                 'b_id',
#                 openapi.IN_PATH,
#                 description='被查询者id',
#                 required=True,
#                 type=openapi.TYPE_INTEGER,
#             ),
#         ],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'note_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='笔记id')
#             }
#         ),
#         responses={200: '成功点赞笔记'}
#     )
#
#     def post(self, request, s_id, b_id):
#         note_id = request.data.get('note_id')
#         note = get_object_or_404(Note, N_id=note_id, S_id=b_id)
#         note.like_num += 1
#         note.save()
#         return Response({'message': 'Successfully liked note.'}, status=status.HTTP_200_OK)
#
#批量导入学生信息
class ImportStudent(APIView):

    @swagger_auto_schema(
        operation_description="批量导入学生信息",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'csv_file': openapi.Schema(type=openapi.TYPE_FILE, description='CSV file')
            }
        ),
        responses={201: '成功导入学生信息'}
    )
    def post(self, request, format=None):
        if 'csv_file' not in request.FILES:
            return Response({"error": "No file part"}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file)

            # 假设CSV文件的列名与模型字段匹配
            students_data = df.to_dict(orient='records')

            for data in students_data:
                student = Student(
                    S_id=data.get('S_id'),
                    account=data.get('account'),
                    password=make_password(data.get('password')),
                    attention_num=data.get('attention_num'),
                    name=data.get('name')
                )  # 解包字典为关键字参数
                student.save()



            return Response({"message": "学生信息导入成功"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 增加学生关注学生
class FollowStudent(APIView):
    @swagger_auto_schema(
        operation_description="增加学生关注学生",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='查询者id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'follow_id',
                openapi.IN_PATH,
                description='被查询者id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={201: '成功关注学生'}
    )

    def post(self, request, s_id, b_id):
        #查询被查询者
        fol=get_object_or_404(Student, pk=b_id)
        fol.attention_num=fol.attention_num+1
        fol.save()
        s=Student.objects.get(S_id=s_id)
        b=Student.objects.get(S_id=b_id)


        follow = StudentStudent(S_id=s, follow=b)
        follow.save()
        return Response({'message': 'Successfully followed student.'}, status=status.HTTP_201_CREATED)


# 获得学生关注的学生
class GetFollowing(APIView):
    @swagger_auto_schema(
        operation_description="获得学生关注的学生",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='查询者id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: '返回学生关注的学生列表'}
    )

    def get(self, request, s_id):
        following = StudentStudent.objects.filter(S_id=s_id)
        return Response({'following': list(following.values('follow'))}, status=status.HTTP_200_OK)


# 取消学生关注的学生
class UnfollowStudent(APIView):
    @swagger_auto_schema(
        operation_description="取消学生关注的学生",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='查询者id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'b_id',
                openapi.IN_PATH,
                description='被查询者id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: '成功取消关注学生'}
    )

    def post(self, request, s_id, follow_id):
        StudentStudent.objects.filter(S_id=s_id, follow=follow_id).delete()
        return Response({'message': 'Successfully unfollowed student.'}, status=status.HTTP_200_OK)


# 学生调整个人信息
class AdjustStudentInfo(APIView):
    @swagger_auto_schema(
        operation_description="学生调整个人信息",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='学生id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account': openapi.Schema(type=openapi.TYPE_STRING, description='新账号'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='新密码')
            }
        ),
        responses={200: '成功更新个人信息'}
    )

    def post(self, request, s_id):
        student = get_object_or_404(Student, pk=s_id)
        account = request.data.get('account')
        password = request.data.get('password')
        print(account)
        print(password)

        if account:
            student.account = account

        if password:
            student.password = make_password(password)

        student.save()
        return Response({'status': 'success', 'message': 'Account and password updated successfully.'},
                        status=status.HTTP_200_OK)


# 验证学生登录
class ValidateStudentLogin(APIView):
    @swagger_auto_schema(
        operation_description="验证学生登录",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account': openapi.Schema(type=openapi.TYPE_STRING, description='账号'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码')
            }
        ),
        responses={200: '成功登录'}
    )

    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        student = Student.objects.filter(account=account).first()
        if student and student.check_password(password):
            return Response({'status': 'success', 'message': 'Login successful.'}, status=status.HTTP_200_OK)
        return Response({'status': 'fail', 'message': 'Invalid username or password.'},
                        status=status.HTTP_401_UNAUTHORIZED)

# from django.contrib.auth.hashers import make_password
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from requests import Response
# from rest_framework.decorators import api_view, action, permission_classes
# from rest_framework.permissions import AllowAny
#
# from student.models import *
#
# @swagger_auto_schema(
#     method='get',
#     operation_description="查询某个学生的所有课程的name,C_id",
#     manual_parameters=[
#         openapi.Parameter(
#             's_id',
#             openapi.IN_PATH,
#             description='学生id',
#             required=True,
#             type=openapi.TYPE_INTEGER,
#         ),
#     ],
#     responses={200: '返回学生的课程列表'}
# )
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def my_course_list(request, s_id):
#     """
#     查询某个学生的所有课程的name,C_id
#
#     :param request: 无
#     :param s_id: 学生id
#     :return: json格式的name,C_id多个数据
#     """
#
#     # 获取学生的所有课程
#     courses = Course.objects.filter(C_id__in=StudentCourse.objects.filter(S_id=s_id).values('C_id'))
#
#     # 将 QuerySet 转换为列表
#     course_names = list(courses.values('name', 'C_id'))
#
#     return JsonResponse({'courses': course_names})
#
#
# #查询某个学生的所有课程通知
# #type=1为课程通知，type=0为系统通知
# @api_view(['GET'])
# def my_course_notice_id(request, s_id):
#     '''
#     查询某个学生的所有课程通知的C_id和对应的I_id
#
#     :param request:无
#
#     :param s_id:学生id
#
#     :return:学生的所有课程通知的C_id和对应的I_id
#     '''
#     res=Releasement.objects.filter(S_id=s_id, type=1)
#     res=res.values('C_id','I_id')
#
#     return JsonResponse({'courses': list(res)})
#
# #根据课程id查询课程名称
# @api_view(['GET'])
# def get_course_name(request, c_id):
#     '''
#     根据课程id查询课程名称
#
#     :param request:无
#
#     :param c_id: 课程id
#
#     :return: json格式的课程名称
#     '''
#     return JsonResponse({'course': list(Course.objects.filter(C_id=c_id).values('name'))})
# #根据通知id查询通知内容
#
# @api_view(['GET'])
# def get_information_content(request, i_id):
#     '''
#     根据通知id查询通知内容
#
#     :param request:无
#
#     :param i_id: 通知id
#
#     :return: json格式的通知内容
#     '''
#     return JsonResponse({'information': list(Information.objects.filter(I_id=i_id).values('content'))})
#
# #查询某个学生的所有系统通知
# @api_view(['GET'])
# def my_system_notice_id(request, s_id):
#     '''
#     查询某个学生的所有系统通知的I_id
#
#     :param request:无
#
#     :param s_id:  学生id
#
#     :return: 学生的所有系统通知的I_id
#     '''
#     res = Releasement.objects.filter(S_id=s_id, type=0)
#     res = res.values('I_id')
#
#     return JsonResponse({'courses': list(res)})
#
#
# #根据账户查询学生
# def get_student_by_account(request):
#     account = request.POST.get('account')
#     return Student.objects.filter(account=account).first()
#
#
#
#
#
# #查询其他学生的所有收藏夹，s_id为查询者id，b_id为被查询者id
# def get_favoritename(request, s_id, b_id):
#
#     fav = Note.objects.filter(N_id__in=Note.objects.filter(S_id=b_id,type=1)).values('favoritename').distinct()
#
#
#     return {'notes': list(fav.values('content'))}
# #获得一个收藏夹的所有笔记
# def get_note_by_favoritename(request, s_id, b_id, favoritename):
#     notes = Note.objects.filter(S_id=b_id, favoritename=favoritename,type=1)
#     return {'notes': list(notes.values('N_id','content'))}
#
# #用户收藏笔记
# def fav_note(request, s_id, b_id):
#     #通过post方法获取笔记id和用户想要保存的收藏夹名
#     fav=request.POST.get('favoritename')
#     #保存后是否可见
#     visible=request.POST.get('type')
#     note_id = request.POST.get('note_id')
#     note = Note.objects.get(N_id=note_id,S_id=b_id)
#     note.fllow_num += 1
#     note.save()
#     #创建一个新的笔记对象
#
#     new_note = Note(
#         S_id=s_id,
#         favoritename=fav,
#         type=visible,
#         addr=note.addr
#     )
#     new_note.save()
#
#
#     return HttpResponse("Successfully liked note.")
# #用户取消收藏笔记
# def unfav_note(request, s_id, b_id):
#     #通过post方法获取笔记id
#     note_id = request.POST.get('note_id')
#     note = Note.objects.get(N_id=note_id,S_id=b_id)
#     note.fllow_num -= 1
#     note.save()
#     return HttpResponse("Successfully unliked note.")
# #用户点赞笔记
# def like_note(request, s_id, b_id):
#     #通过post方法获取笔记id
#     note_id = request.POST.get('note_id')
#     note = Note.objects.get(N_id=note_id,S_id=b_id)
#     note.like_num += 1
#     note.save()
#     return HttpResponse("Successfully liked note.")
#
#
#
# #批量导入学生信息
#
# def import_student(request):
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#
#         try:
#             # 使用 pandas 读取 Excel 文件
#             df = pd.read_excel(excel_file)
#
#             # 根据 DataFrame 创建学生记录
#             students_created = []
#             for index, row in df.iterrows():
#                 student = Student(
#                     S_id=row['S_id'],
#                     name=row['name'],
#                     attention_num=row['attention_num'],
#                     account=row['account'],
#                     password=row['password']
#
#                 )
#                 student.save()
#                 students_created.append(student)
#
#             message = f"{len(students_created)} students were successfully created."
#             return HttpResponse(message)
#         except Exception as e:
#             error_message = f"Failed to import data: {str(e)}"
#             return HttpResponse(error_message, status=500)
#     else:
#         return render(request, 'import_students.html')
#
# #增加学生关注学生
# def follow_student(request, s_id, follow_id):
#     # 创建关注关系
#     follow = StudentStudent(S_id=s_id, follow=follow_id)
#     follow.save()
#     return HttpResponse("Successfully followed student.")
# #获得学生关注的学生
# def get_following(request, s_id):
#     following = StudentStudent.objects.filter(S_id=s_id)
#     return {'following': list(following.values('follow'))}
# #取消学生关注的学生
# def unfollow_student(request, s_id, follow_id):
#     # 删除关注关系
#     StudentStudent.objects.filter(S_id=s_id, follow=follow_id).delete()
#     return HttpResponse("Successfully unfollowed student.")
#
# #学生调整个人信息
# def adjust_student_info(request, s_id):
#     if request.method == 'POST':
#         # 获取学生对象
#         student = get_object_or_404(Student, pk=s_id)
#
#         # 从 POST 请求中获取新信息
#         account = request.POST.get('account')
#         password = request.POST.get('password')
#
#         # 更新学生信息
#         if account:
#             student.account = account
#
#         if password:
#             # 对密码进行加密处理
#             student.password = make_password(password)
#
#         student.save()
#
#         # 返回成功信息或重定向到另一个页面
#         return JsonResponse({'status': 'success', 'message': 'Account and password updated successfully.'})
#     else:
#         # 如果是 GET 请求，则渲染表单页面
#         return JsonResponse({'status': 'fail', 'message': 'Account and password updated fail.'})
# #验证学生登录
# def validate_student_login(request):
#     if request.method == 'POST':
#         # 从 POST 请求中获取用户名和密码
#
#         account = request.POST.get('account')
#         password = request.POST.get('password')
#
#         # 在数据库中查找学生
#         student = Student.objects.filter(account=account).first()
#
#         # 验证学生密码
#         if student and student.check_password(password):
#             return JsonResponse({'status': 'success', 'message': 'Login successful.'})
#         else:
#             return JsonResponse({'status': 'fail', 'message': 'Invalid username or password.'})
#     else:
#         return render(request, 'login.html')
