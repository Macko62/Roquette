from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import mdlSignMessages as model
from .serializers import smSerializer as serializer

BAD_REQUEST=status.HTTP_400_BAD_REQUEST
OK=status.HTTP_200_OK
CREATED=status.HTTP_201_CREATED
NOT_ACCEPTABLE=status.HTTP_406_NOT_ACCEPTABLE

@api_view(['GET', ])
def api_get(request):
    if request.method=='GET':
        data=model.objects.all()
        s=serializer(data,many=True)
        return Response(s.data,status=OK)
    else: return Response('invalid method',status=BAD_REQUEST)

@api_view(['PUT'])
def api_put(request):
    if request.method=='PUT':
        msgNum=int(request.POST['msgNum'])+int(model.objects.first().id)-1
        m=model.objects.get(id=msgNum)
        s=serializer(m,data=request.data)
        if s.is_valid(): 
            s.save()
            return Response(s.data,status=CREATED)
        else: return Response(s.error,status=NOT_ACCEPTABLE)
    else: return Response('invalid method',status=BAD_REQUEST)

