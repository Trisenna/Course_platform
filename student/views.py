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
        #根据I_id查到通知内容
        for notice in notices:
            information = Information.objects.filter(I_id=notice['I_id']).values('content').first()
            notice['information'] = information
        return Response({'notices': list(notices)}, status=status.HTTP_200_OK)


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
                #为每个学生创建一个文件夹用于存放收藏夹
                #在favorite文件夹下创建一个以学生id命名的文件夹
                os.makedirs(f'favorite/{data.get("S_id")}')



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
        #根据id查询关注的学生
        students = Student.objects.filter(S_id__in=following.values('follow'))
        return Response({'students': list(students.values('S_id', 'name'))}, status=status.HTTP_200_OK)



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

    def post(self, request, s_id, b_id):
        StudentStudent.objects.filter(S_id=s_id, follow=b_id).delete()
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

        if account:
            student.account = account

        if password:
            student.password = password

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
        student = Student.objects.filter(account=account, password=password).first()
        if student:
            return Response({'status': 'success', 'message': 'Login successful.','s_id':student.S_id}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'message': 'Login failed.'}, status=status.HTTP_401_UNAUTHORIZED)
#用户自己创建收藏夹
class CreateFavorite(APIView):
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
    @swagger_auto_schema(
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
#用户下载自己的笔记
class DownloadNote(APIView):
    @swagger_auto_schema(
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
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='笔记title')
            }
        ),
        responses={200: '成功下载笔记'}
    )

    def post(self, request, s_id):
        title = request.data.get('title')
        s_id=Student.objects.get(S_id=s_id)
        note = Note.objects.get(F_id__S_id=s_id, title=title)
        file = note.file
        #返回文件

        return Response({'file': file}, status=status.HTTP_200_OK)
#用户下载他人的笔记
class DownloadNote_other(APIView):
    @swagger_auto_schema(
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
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='笔记title')
            }
        ),
        responses={200: '成功下载笔记'}
    )

    def post(self, request, s_id, b_id):
        title = request.data.get('title')
        b_id=Student.objects.get(S_id=b_id)
        note = Note.objects.get(F_id__S_id=b_id, title=title)
        file = note.file
        return Response({'file': file}, status=status.HTTP_200_OK)










