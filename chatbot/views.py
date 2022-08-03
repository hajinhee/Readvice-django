from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


@api_view(["GET", "POST"])
@parser_classes([JSONParser])
def chatbot(request):
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
    except User.DoesNotExist:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)