import json

import requests
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db.models.functions import NullIf
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from global_models.models import Student, Teacher, Admin, User # 确保正确导入您的模型

# 用户登录
class Login(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account': openapi.Schema(type=openapi.TYPE_STRING, description='账号'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='token'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户ID'),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='姓名'),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='角色'),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='错误信息'),
                }
            )
        },
        operation_summary='登录',
        operation_description='登录接口'
    )
    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')




        # 使用 Django 的 authenticate 方法验证用户
        #手动查找用户
        user = authenticate(username=account, password=password)

        if user is not None:
            try:
                # 根据关联的 User 查找对应的 Student, Teacher 或 Admin
                student = Student.objects.get(user=user)
                role = "student"
                id_field = 'S_id'
            except Student.DoesNotExist:
                try:
                    teacher = Teacher.objects.get(user=user)
                    role = "teacher"
                    id_field = 'T_id'
                except Teacher.DoesNotExist:
                    try:
                        admin = Admin.objects.get(user=user)
                        role = "admin"
                        id_field = 'A_id'
                    except Admin.DoesNotExist:
                        return Response({'message': '无效的凭证'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取或创建 Token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id': getattr(locals()[role], id_field),
                'name': getattr(locals()[role], 'name'),
                'role': role,
            }, status=status.HTTP_200_OK)

        # 如果认证失败
        return Response({'message': '无效的凭证'}, status=status.HTTP_400_BAD_REQUEST)

# 用户重置密码
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary='用户重置密码',
        operation_description="根据用户输入的账号与手机号是否匹配重置密码",
        manual_parameters=[
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account': openapi.Schema(type=openapi.TYPE_STRING, description='用户账号'),
                'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING, description='用户手机号'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='新密码'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='确认密码'),
            },
        ),
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='密码重置成功'),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='错误信息'),
                }
            )
        },
    )
    def post(self, request):
        account = request.data.get('account')
        phoneNumber = request.data.get('phoneNumber')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 检查用户的账号、手机号、新密码和确认密码是否全部输入
        if account is None or account == '':
            return Response({'message': 'Account is required'}, status=status.HTTP_400_BAD_REQUEST)
        if phoneNumber is None or phoneNumber == '':
            return Response({'message': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password is None or new_password == '':
            return Response({'message': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if confirm_password is None or confirm_password == '':
            return Response({'message': 'Confirm_password is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查新密码和确认密码是否一致
        if new_password != confirm_password:
            return Response({'message': 'The new password is different from the confirmed password.'}, status=status.HTTP_400_BAD_REQUEST)

        # 查找用户
        try:
            user = User.objects.get(username=account)
        except User.DoesNotExist:
            return Response({'message': 'Account does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # 查找关联的角色
        try:
            if hasattr(user, 'student'):
                role_instance = user.student
                role_phone = role_instance.phoneNumber
            elif hasattr(user, 'teacher'):
                role_instance = user.teacher
                role_phone = role_instance.phoneNumber
            else:
                return Response({'message': 'User role not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({'message': '用户角色关联出错'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证手机号
        if phoneNumber != role_phone:
            return Response({'message': 'Phone number is wrong, please re-enter'}, status=status.HTTP_400_BAD_REQUEST)

        # 更新密码
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Reset password successfully.'}, status=status.HTTP_201_CREATED)

from MyWork.service import BaiduApiService


@api_view(['GET'])
def call_baidu_api(request):
    user_input = request.query_params.get('userInput', None)

    if user_input is None:
        return Response({"error": "Missing userInput parameter"}, status=status.HTTP_400_BAD_REQUEST)

    baidu_api_service = BaiduApiService()
    try:
        result = baidu_api_service.call_api(user_input)
        print(result)
        return Response(json.loads(result))  # 假设返回的是JSON格式的数据
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)