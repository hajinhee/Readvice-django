from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def hello_api(request):
    print("####### 서버로 들어옴 #######")
    return Response({'message': datetime.now()})
