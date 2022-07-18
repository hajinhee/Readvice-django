from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from comments.models import Comment
from comments.serializers import CommentSerializer
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer


@api_view(["GET", "POST", "PUT", "DELETE"])
@parser_classes([JSONParser])
def write(request):
    print('1 comments 로 들어옴')
    try:
        comments = Comment.objects.all()
        if request.method == 'GET':
            print('2 GET 으로 들어옴')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            print('2 POST 로 들어옴')
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print('3. 들어온 내부값: ', serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print('error: ', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            print('2 PUT 으로 들어옴')
            serializer = CommentSerializer(comments, data=request.data)
            if serializer.is_valid():
                comments.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            comments.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@parser_classes([JSONParser])
def mypage(request):
    queryset = Comment.objects.all()
    serializer = CommentSerializer(queryset, many=True)
    return Response(serializer.data)

