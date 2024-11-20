import os

import pandas as pd
from django.contrib.auth.hashers import make_password
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema



from global_models.models import *


class MyCourseList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_summary='查询某个学生的所有课程的名字',
        operation_description="查询某个学生的所有课程的name, C_id",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='学生id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: '返回学生的课程列表', 404: '学生不存在'}
    )
    def get(self, request, s_id):
        # 检查学生是否存在
        if not StudentCourse.objects.filter(S_id=s_id).exists():
            raise NotFound(detail="学生不存在")

        # 获取该学生选修的所有课程的ID
        student_courses = StudentCourse.objects.filter(S_id=s_id).values_list('C_id', flat=True)

        # 根据课程ID查询课程的名称和ID
        courses = Course.objects.filter(C_id__in=student_courses).values('name', 'C_id')

        return Response({'courses': list(courses)}, status=status.HTTP_200_OK)
# 查询某个学生的所有课程通知
class MyCourseNotice(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查询某个学生的所有课程通知',
        operation_description="查询某个学生的所有课程通知的C_id和对应的I_id,type=1",
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
        #根据C_id查到课程名，根据I_id查到通知内容
        for notice in notices:
            course = Course.objects.filter(C_id=notice['C_id']).values('name').first()
            information = Information.objects.filter(I_id=notice['I_id']).values('content').first()
            notice['course'] = course
            notice['information'] = information


        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)



# 查询某个学生的所有系统通知
class MySystemNotice(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary= '查询某个学生的所有系统通知',
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
        #根据I_id查到通知内容
        for notice in notices:
            information = Information.objects.filter(I_id=notice['I_id']).values('content').first()
            notice['information'] = information
        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)


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
                #为每个学生创建一个文件夹用于存放收藏夹
                #在favorite文件夹下创建一个以学生id命名的文件夹
                os.makedirs(f'favorite/{data.get("S_id")}')



            return Response({"message": "学生信息导入成功"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 增加学生关注学生
class FollowStudent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='增加学生关注学生',
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
                'b_id',
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='获得学生关注的学生',
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
        #根据id查询关注的学生
        students = Student.objects.filter(S_id__in=following.values('follow'))
        return Response({'students': list(students.values('S_id', 'name'))}, status=status.HTTP_200_OK)



# 取消学生关注的学生
class UnfollowStudent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='取消学生关注的学生',
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

    def post(self, request, s_id, b_id):
        StudentStudent.objects.filter(S_id=s_id, follow=b_id).delete()
        return Response({'message': 'Successfully unfollowed student.'}, status=status.HTTP_200_OK)


# 学生调整个人信息
class AdjustStudentInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='学生调整个人信息',
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

        if account:
            student.account = account

        if password:
            student.password = password

        student.save()
        return Response({'status': 'success', 'message': 'Account and password updated successfully.'},
                        status=status.HTTP_200_OK)


class ValidateStudentLogin(APIView):

    @swagger_auto_schema(
        operation_summary='验证学生登录',
        operation_description="验证学生登录",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account': openapi.Schema(type=openapi.TYPE_STRING, description='账号'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码')
            }
        ),
        responses={200: '成功登录', 401: '登录失败'}
    )
    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        student = Student.objects.filter(account=account, password=password).first()

        if student:
            token, created = Token.objects.get_or_create(user=student)
            return Response({'s_id': student.S_id, 'token': token.key}, status=status.HTTP_200_OK)

        return Response({'status': 'error', 'message': 'Login failed.'}, status=status.HTTP_401_UNAUTHORIZED)
#用户自己创建收藏夹
class CreateFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户自己创建收藏夹',
        operation_description="用户自己创建收藏夹",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名'),
                'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='保存后是否可见'),
            }
        ),
        responses={201: '成功创建收藏夹', 400: 'Favorite name already exists.'}

    )

    def post(self, request, s_id):
        name = request.data.get('name')
        visible = request.data.get('type')

        #查询Fava中所有s_id为s_id的数据
        favs = Favorite.objects.filter(S_id=s_id).values('name')
        #判断是否有重名的收藏夹
        for fav in favs:
            if fav['name'] == request.data.get('name'):
                return Response({'error': 'Favorite name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        s=Student.objects.get(S_id=s_id)
        new_fav = Favorite(
        S_id=s,
        name = name,

        type = visible,
        # 链接到F_id
        link = None,
        follow_num = 0,
        like_num = 0
        )

        new_fav.save()
        #为在这个学生的文件夹下创建一个以收藏夹名命名的文件夹
        os.makedirs(f'favorite/{s_id}/{name}')
        return Response({'message': 'Successfully created favorite.'}, status=status.HTTP_201_CREATED)
# 用户收藏其他人的收藏夹
class FavFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户收藏其他人的收藏夹',
        operation_description="用户收藏其他人的收藏夹",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'b_name': openapi.Schema(type=openapi.TYPE_STRING, description='被收藏的收藏夹名'),
                'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='保存后是否可见'),
                's_name': openapi.Schema(type=openapi.TYPE_STRING, description='收藏后的收藏夹名')

            }
        ),
        responses={201: '成功收藏收藏夹'}
    )

    def post(self, request, s_id, b_id):
        b_name = request.data.get('b_name')
        visible = request.data.get('type')
        s_name = request.data.get('s_name')

        b_id=Student.objects.get(S_id=b_id)
        s_id=Student.objects.get(S_id=s_id)

        favorite = get_object_or_404(Favorite, name=b_name, S_id=b_id)
        favorite.follow_num += 1
        favorite.save()


        new_favorite = Favorite(
            S_id=s_id,
            name=s_name,
            type=visible,
            link=favorite
        )
        new_favorite.save()

        return Response({'message': 'Successfully liked favorite.'}, status=status.HTTP_201_CREATED)

# 用户删除收藏夹
class UnfavFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户删除收藏夹',
        operation_description="用户删除收藏夹",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='查询者id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),

        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_INTEGER, description='收藏夹名称')
            }
        ),
        responses={200: '成功删除收藏夹'}
    )

    def post(self, request, s_id):
        name = request.data.get('name')
        print(name)
        s_id=Student.objects.get(S_id=s_id)
        favorite = get_object_or_404(Favorite, name=name, S_id=s_id)
        #获得链接的收藏夹
        link = favorite.link
        if link:
            link.follow_num -= 1
            link.save()
        else:
            #如果没有链接的收藏夹，直接删除此收藏夹路径下的所有文件
            os.removedirs(f'favorite/{s_id}/{name}')

        favorite.delete()
        return Response({'message': 'Successfully unliked favorite.'}, status=status.HTTP_200_OK)
#用户删除收藏的收藏夹
class UnfavFavorite_id(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户删除收藏的收藏夹',
        operation_description="用户在其他人的界面删除收藏夹",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_INTEGER, description='收藏夹名称')
            }
        ),
        responses={200: '成功删除收藏夹'}
    )

    def post(self, request, s_id,b_id):
        name = request.data.get('name')
        b_id=Student.objects.get(S_id=b_id)
        s_id=Student.objects.get(S_id=s_id)
        favorite = get_object_or_404(Favorite, name=name, S_id=b_id)
        favorite.follow_num -= 1
        favorite.save()
        favorite1=Favorite.objects.get(S_id=s_id,link=favorite)
        favorite1.delete()
        return Response({'message': 'Successfully unliked favorite.'}, status=status.HTTP_200_OK)
# 用户点赞收藏夹
class LikeFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户点赞收藏夹',
        operation_description="用户点赞收藏夹",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名')
            }
        ),
        responses={200: '成功点赞收藏夹'}
    )

    def post(self, request, s_id, b_id):
        name = request.data.get('name')
        b_id=Student.objects.get(S_id=b_id)
        favorite = get_object_or_404(Favorite, name=name, S_id=b_id)
        favorite.like_num += 1
        favorite.save()
        s_id=Student.objects.get(S_id=s_id)
        like=Like(S_id=s_id,F_id=favorite)
        like.save()
        return Response({'message': 'Successfully liked favorite.'}, status=status.HTTP_200_OK)
# 用户取消点赞收藏夹
class UnlikeFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户取消点赞收藏夹',
        operation_description="用户取消点赞收藏夹",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名')
            }
        ),
        responses={200: '成功取消点赞收藏夹'}
    )

    def post(self, request, s_id, b_id):
        name = request.data.get('name')
        b_id=Student.objects.get(S_id=b_id)
        favorite = get_object_or_404(Favorite, name=name, S_id=b_id)
        favorite.like_num -= 1
        favorite.save()
        like=Like.objects.filter(S_id=s_id,F_id=favorite)
        like.delete()
        return Response({'message': 'Successfully unliked favorite.'}, status=status.HTTP_200_OK)
#判断用户是否收藏了某个用户的收藏夹
class IsFavFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='判断用户是否收藏了某个用户的收藏夹',
        operation_description="判断用户是否收藏了某个用户的收藏夹",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名')
            }
        ),
        responses={200: '返回是否收藏'}
    )

    def post(self, request, s_id, b_id):
        name = request.data.get('name')
        b_id=Student.objects.get(S_id=b_id)

        favorite = Favorite.objects.filter(name=name, S_id=b_id).first()
        s_id=Student.objects.get(S_id=s_id)
        fa=Favorite.objects.filter(S_id=s_id,link=favorite).first()
        if fa:
            return Response({'is_fav': True}, status=status.HTTP_200_OK)
        return Response({'is_fav': False}, status=status.HTTP_200_OK)
#判断用户是否点赞了某个用户的收藏夹
class IsLikeFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="判断用户是否点赞了某个用户的收藏夹",
        operation_description="判断用户是否点赞了某个用户的收藏夹",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名')
            }
        ),
        responses={200: '返回是否点赞'}
    )

    def post(self, request, s_id, b_id):
        name = request.data.get('name')
        s_id=Student.objects.get(S_id=s_id)
        b_id=Student.objects.get(S_id=b_id)

        favorite = Favorite.objects.filter( name=name, S_id=b_id).first()
        like=Like.objects.filter(S_id=s_id,F_id=favorite).first()
        if like:
            return Response({'is_like': True}, status=status.HTTP_200_OK)
        return Response({'is_like': False}, status=status.HTTP_200_OK)

#用户查询个人信息
class GetStudentInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户查询个人信息',
        operation_description="用户查询个人信息",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: '返回个人信息'}
    )

    def get(self, request, s_id):
        student = get_object_or_404(Student, pk=s_id)
        return Response({'student': {'account': student.account,'password':student.password, 'name': student.name}}, status=status.HTTP_200_OK)

#查看自己的收藏夹
class GetFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看自己的收藏夹',
        operation_description="查看自己的收藏夹",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: '返回收藏夹列表'}
    )

    def get(self, request, s_id):
        s_id=Student.objects.get(S_id=s_id)
        favorites = Favorite.objects.filter(S_id=s_id)
        return Response({'favorites': list(favorites.values('name', 'type','F_id'))}, status=status.HTTP_200_OK)
#查看自己收藏夹中的笔记
class GetNoteInFavorite(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看自己收藏夹中的笔记',
        operation_description="查看自己收藏夹中的笔记",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'favname': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名')
            }
        ),
        responses={200: '返回笔记列表'}
    )

    def post(self, request, s_id):
        favname = request.data.get('favname')
        s_id=Student.objects.get(S_id=s_id)
        favorite = Favorite.objects.get(S_id=s_id, name=favname)
        notes = Note.objects.filter(F_id=favorite)
        return Response({'notes': list(notes.values('N_id', 'title'))}, status=status.HTTP_200_OK)
#用户获取他人的收藏夹
class GetFavorite_other(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户获取他人的收藏夹',
        operation_description="用户获取他人的收藏夹",
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
        responses={200: '返回收藏夹列表'}
    )

    def get(self, request, s_id, b_id):
        b_id=Student.objects.get(S_id=b_id)
        favorites = Favorite.objects.filter(S_id=b_id,type=1)
        return Response({'favorites': list(favorites.values('name', 'type','F_id'))}, status=status.HTTP_200_OK)
#用户获取他人的收藏夹中的笔记title
class GetNoteInFavorite_other(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户获取他人的收藏夹中的笔记title',
        operation_description="用户获取他人的收藏夹中的笔记title",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'favname': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名')
            }
        ),
        responses={200: '返回笔记列表'}
    )

    def post(self, request, s_id, b_id):
        favname = request.data.get('favname')
        b_id=Student.objects.get(S_id=b_id)
        favorite = Favorite.objects.get(S_id=b_id, name=favname)
        notes = Note.objects.filter(F_id=favorite)
        return Response({'notes': list(notes.values('N_id', 'title'))}, status=status.HTTP_200_OK)
#用户上传笔记
class UploadNote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户上传笔记',
        operation_description="用户上传笔记",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='笔记标题'),
                'favname': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='文件')
            }
        ),
        responses={201: '成功上传笔记'}
    )

    def post(self, request, s_id):
        title = request.data.get('title')
        favname = request.data.get('favname')
        file = request.data.get('file')
        s_id=Student.objects.get(S_id=s_id)
        favorite = Favorite.objects.get(S_id=s_id, name=favname)
        #查询是否有重名的笔记
        notes = Note.objects.filter(F_id=favorite)
        for note in notes:
            if note.title == title:
               #删除文件和对应的记录

                os.remove(note.file.__str__())
                note.delete()

        note = Note(
            title=title,
            F_id=favorite,
            file=file
        )
        note.save()
        return Response({'message': 'Successfully uploaded note.'}, status=status.HTTP_201_CREATED)
#用户删除笔记
class DeleteNote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='用户删除笔记',
        operation_description="用户删除笔记",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_INTEGER, description='笔记title')
            }
        ),
        responses={200: '成功删除笔记'}
    )

    def post(self, request, s_id):
        title = request.data.get('title')
        s_id=Student.objects.get(S_id=s_id)
        note = Note.objects.get(F_id__S_id=s_id, title=title)
        #删除文件和对应的记录
        os.remove(note.file.__str__())
        note.delete()
        return Response({'message': 'Successfully deleted note.'}, status=status.HTTP_200_OK)


class DownloadBase:
    def download_file(self, note):
        """
        处理文件下载的逻辑。

        :param note: 笔记对象
        :return: 文件下载响应
        """
        file_path = note.file.path
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
class DownloadNote(APIView, DownloadBase):
    @swagger_auto_schema(
        operation_summary='用户下载笔记',
        operation_description="用户下载笔记",
        manual_parameters=[
            openapi.Parameter(
                's_id',
                openapi.IN_PATH,
                description='用户id',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'favname': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='笔记title')
            }
        ),
        responses={200: '成功下载笔记'}
    )

    def post(self, request, s_id):
        favname = request.data.get('favname')
        title = request.data.get('title')
        s_id=Student.objects.get(S_id=s_id)
        favorite = Favorite.objects.get(S_id=s_id, name=favname)
        note = Note.objects.get(F_id=favorite, title=title)
        return self.download_file(note)


#用户下载他人的笔记
class DownloadNote_other(APIView, DownloadBase):
    @swagger_auto_schema(
        operation_summary='用户下载他人的笔记',
        operation_description="用户下载他人的笔记",
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
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'favname': openapi.Schema(type=openapi.TYPE_STRING, description='收藏夹名'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='笔记title')
            }
        ),
        responses={200: '成功下载笔记'}
    )

    def post(self, request, s_id, b_id):
        favname = request.data.get('favname')
        title = request.data.get('title')
        b_id=Student.objects.get(S_id=b_id)
        favorite = Favorite.objects.get(S_id=b_id, name=favname)
        note = Note.objects.get(F_id=favorite, title=title)
        return self.download_file(note)
#查看课程大纲
class GetCourseOutline(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看课程大纲',
        operation_description='允许学生通过课程id来查看该课程的课程大纲。',
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

    def post(self, request, s_id):
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
        operation_description='允许学生通过课程id来查看该课程的课程介绍。',
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

    def post(self, request, s_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            return Response({"introduction": course.introduction})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

class GetCourseCalendar(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看教学日历',
        operation_description='允许学生通过课程id来查看该课程的教学日历。',
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
#查看课程教师的信息
class GetCourseTeacherInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看课程教师的信息',
        operation_description='允许学生通过课程id来查看该课程的教师信息。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回教师信息'
            )
        }
    )

    def post(self, request, s_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            teacher = CourseTeacher.objects.get(C_id=course).T_id
            return Response({"teacher name": teacher.name})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)

#教师查看课件
class GetCourseMaterial(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='查看课件',
        operation_description='允许学生通过课程id来查看该课程的课件。',
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

    def post(self, request, s_id):
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
        operation_description='允许学生通过课程id来查看该课程的试题。',
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

    def post(self, request, s_id):
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
        operation_description='允许学生通过课程id来查看该课程的习题。',
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

    def post(self, request, s_id):
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
#学生查看自己某个课程的所有作业
class GetAllwork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='学生查看自己某个课程的所有作业',
        operation_description='允许学生通过课程id来查看该课程的作业。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'c_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='课程id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回作业',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/homework.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, s_id):
        c_id = request.data.get('c_id')
        if c_id is None:
            return Response({"error": "课程id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(C_id=c_id)
            student=Student.objects.get(S_id=s_id)
            # 获取课程的作业资源
            W_id = DoWork.objects.filter(C_id=course, S_id=student).values("W_id")
            if W_id is None:
                return Response({"error": "作业不存在"}, status=status.HTTP_404_NOT_FOUND)
            #获取作业的title

            title=Work.objects.filter(W_id__in=W_id).values("title","W_id")
            return Response({"title": title})
        except Course.DoesNotExist:
            return Response({"error": "课程不存在"}, status=status.HTTP_404_NOT_FOUND)
#学生查看自己的某个作业
class GetWork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='学生查看自己的某个作业',
        operation_description='允许学生通过作业id来查看该作业的内容。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'w_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='作业id'),
            }
        ),
        responses={
            200: openapi.Response(
                '返回作业',
                examples={
                    "application/json": {
                        "download_link": "http://example.com/download/path/to/work.pdf"
                    }
                }
            )
        }
    )

    def post(self, request, s_id):
        w_id = request.data.get('w_id')
        if w_id is None:
            return Response({"error": "作业id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            work = Work.objects.get(W_id=w_id).content
            # 假设file字段保存的是文件路径
            file_path = work.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Work.DoesNotExist:
            return Response({"error": "作业不存在"}, status=status.HTTP_404_NOT_FOUND)
#学生提交作业
class SubmitWork(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary='学生提交作业',
        operation_description='允许学生通过作业id来提交该作业。',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'w_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='作业id'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='文件')
            }
        ),
        responses={
            201: '成功提交作业'
        }
    )

    def post(self, request, s_id):
        w_id = request.data.get('w_id')
        file = request.data.get('file')
        if w_id is None:
            return Response({"error": "作业id未提供"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(S_id=s_id)
            work = Work.objects.get(W_id=w_id)
            w=DoWork.objects.get(S_id=student,W_id=work)
            w.file=file
            w.is_push=True
            w.save()

            return Response({"message": "成功提交作业"}, status=status.HTTP_201_CREATED)
        except Work.DoesNotExist:
            return Response({"error": "作业不存在"}, status=status.HTTP_404_NOT_FOUND)















