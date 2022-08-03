from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from kogpt2.models import Solution


@api_view(["POST"])
@parser_classes([JSONParser])
def generate(request):
    print('1 autowrite 로 들어옴')
    try:
        if request.method == 'POST':
            print('2 POST 으로 들어옴')
            text = request.data.get('book')
            print(text)
            generate = Solution(text).result()
            return Response({generate})
    except:
        return Response({"Message":"독서 기록 생성 실패"})