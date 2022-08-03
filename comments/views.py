from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser

from books.models import Book
from books.serializers import BookSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer, MypageSerializer
from rest_framework.response import Response
from users.models import User


@api_view(["GET", "POST", "PUT", "DELETE"])
@parser_classes([JSONParser])
def write(request):
    print('1 comments 로 들어옴')
    try:
        if request.method == 'GET':
            print('2 GET 으로 들어옴')
            comments = Comment.objects.all()
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
            comment_id = request.data.get('comment_id', None)
            comment = get_object_or_404(Comment, comment_id=comment_id)
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            comment_id = request.data.get('comment_id', None)
            comment = get_object_or_404(Comment, comment_id=comment_id)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST", "DELETE"])
@parser_classes([JSONParser])
def mypage(request):
    print('1 mypage 로 들어옴')
    try:
        if request.method == 'GET':
            print("2. GET 들어옴")
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            print("2. POST 들어옴")
            serializer = BookSerializer(data=request.data)
            print('serializer', serializer)
            if serializer.is_valid():
                serializer.save()
                print('3. 들어온 내부값:', serializer)
                return Response(serializer.data, status=200)
        elif request.method == 'DELETE':
            isbn = request.data.get('isbn', None)
            mypage = get_object_or_404(Book, isbn=isbn)
            mypage.delete()
        return Response({'books': 'fail'})
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@parser_classes([JSONParser])
def all_info(request):
    queryset = User.objects.raw('SELECT * FROM users LEFT JOIN comments ON users.email = comments.email_id '
                                'RIGHT JOIN books ON comments.isbn_id=books.isbn')
    serializer = MypageSerializer(queryset, many=True)
    return Response(serializer.data)