from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer


@api_view(["GET", "POST", "DELETE"])
@parser_classes([JSONParser])
def info(request):
    print("1.books로 들어옴")
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
            # books = Book.objects.all()
            # books.delete()
            # data={
            #     'isbn_pk': isbn_pk
            # }
            return Response({'books': 'fail'})
    except:
        return JsonResponse({'books': 'fail'})