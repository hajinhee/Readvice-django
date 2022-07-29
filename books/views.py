from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer, UploadSerializer


@api_view(["GET"])
@parser_classes([JSONParser])
def search(request):
    print("1.books로 들어옴")
    try:
        if request.method == 'GET':
            print("2. GET 들어옴")
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
    except:
        return JsonResponse({'books': 'fail'})


@api_view(["GET", "POST"])
@parser_classes([JSONParser])
def upload_files(request):
    print('1 upload 로 들어옴')
    book_title = request.data.get('book_title')  # 클라이언트 요청 이메일
    try:
        if request.method == 'GET':
            print('2 GET 으로 들어옴')
            book = get_object_or_404(Book, book_title=book_title)
            serializer = UploadSerializer(book, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            print(f'2 POST 로 들어옴')
            # print('request_data: ', request.data)
            serializer = UploadSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  # raise된 에러를 가시적으로 클라이언트에 전달
                # print(serializer)
                # print('3. 들어온 내부값: ', serializer.data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print('error: ', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        print('#############4')
        return Response({"Message": f"{book_title}에 대한 검색결과가 없습니다."})
