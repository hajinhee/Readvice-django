from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response
from books.models import Book
from books.serializers import BookSerializer
import json
import pandas as pd

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


@api_view(["POST"])
@parser_classes([JSONParser])
def add_test(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print('3. 들어온 내부값: ', serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('error: ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



