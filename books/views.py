from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer


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

