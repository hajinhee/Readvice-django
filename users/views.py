from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import  User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response


@api_view(["GET", "POST", "PUT", "DELETE"])
@parser_classes([JSONParser])
def users(request):
    print('1 users 로 들어옴')
    try:
        if request.method == 'GET':
            print('2 GET 으로 들어옴')
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            print(f'2 POST 로 들어옴')
            # print('request_data: ', request.data)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  # raise된 에러를 가시적으로 클라이언트에 전달
                # print(serializer)
                # print('3. 들어온 내부값: ', serializer.data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print('error: ', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            print('2 PUT 으로 들어옴')
            email = request.data.get('email', None)
            user = get_object_or_404(User, email=email)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            email = request.data.get('email', None)
            user = get_object_or_404(User, email=email)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@parser_classes([JSONParser])
def login(request):
    print(f'1 login 로 들어옴')
    email = request.data.get('email')  # 클라이언트 요청 이메일
    # print(f'2 email: {email}')
    password = request.data.get('password')
    # print(f'3 password: {password}')

    # db_email = User.objects.get(email=email).email
    # print(f'5 db_email: {db_email}')
    try:
        if email == User.objects.get(email=email).email:
            if password == User.objects.get(email=email).password:
                return Response({"Message": "로그인 성공"})
            else:
                return Response({"Message": "비밀번호 오류"})
    except User.DoesNotExist:
        return Response({"Message": "존재하지 않는 아이디"})

    #     authenticated_user = authenticate(request, username=username, password=password)
    #     print(authenticated_user)
    #     if authenticated_user is not None:
    #         if (authenticated_user.is_authenticated and authenticated_user.is_superuser):
    #             login(request, authenticated_user)
    #             print('1request: ', request.data)
    #             print('1authenticated_user: ', authenticated_user)
    #             print("User is Authenticated.")
    #             return Response({"Message": "User is Authenticated. "})
    #         else:
    #             print('2request: ', request.data)
    #             print('2authenticated_user: ', authenticated_user)
    #             print("User is not authenticated.")
    #             return Response({"message": "User is not authenticated. "})
    #     else:
    #         print('3request: ', request.data)
    #         print('3authenticated_user: ', authenticated_user)
    #         print("Either User is not registered or password does not match")
    #         return Response({"Message": "Either User is not registered or password does not match"})
    # except User.DoesNotExist:
    #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@parser_classes([JSONParser])
def logout(request):
    print(request.user)
    logout(request)
    return Response({"message": "LoggedOut"})
