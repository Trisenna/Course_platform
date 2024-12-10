from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from global_models.models import Student, Teacher, Admin  # 确保正确导入您的模型

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