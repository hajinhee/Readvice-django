from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer
from ocr.models import Solution

@api_view(["POST"])
@parser_classes([MultiPartParser])
def read_image(request):
    print('1 read_image 로 들어옴')
    try:
        if request.method == 'POST' and request.FILES['book_img']:
            print('2 POST로 들어옴')
            book_img = request.FILES['book_img']
            fs = FileSystemStorage(location='media/images', base_url='media/images')
            # FileSystemStorage.save(file_name, file_content)
            filename = fs.save(book_img.name, book_img)
            save_img_url = fs.url(filename)
            book_title = Solution(save_img_url).solution()
            print('*******book_title: ', book_title[0])
            result = book_title[0]

            return Response({result})

            # Book.book_img = request.FILES['book_img']
            # print('1')
            # serializer = SolutionSerializer(data=request.data)
            # if serializer.is_valid():
            #     print('2')
            #
            #     upload_img = serializer.save()
            #     redirect('./images/upload_img.jpg', upload_img)
            #     save_img = './images/upload_img.jpg'
            #     book_title = Solution(save_img)
            #     serializer = SolutionSerializer(book_title, many=True)
            #     return Response(serializer.data)
    except:
        return Response({"Message": "해당 표지의 제목을 읽을 수 없습니다."})
