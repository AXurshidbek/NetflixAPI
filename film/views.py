from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

class HelloAPI(APIView):
    def get(self,request):
        d={
            "xabar":"Assalomu alaykum",
            "izoh":"Test uchun API"
        }
        return Response(d)
    def post(self,request):
        d=request.data
        natja={
            "xabar":"Post qabul qilindi",
            "post ma'lumoti" : d
        }
        return Response(d)

class AktyorlarAPI(APIView):
    def get(self,request):
        aktyorlar=Aktyor.objects.all()
        serializer=AktyorSerializer(aktyorlar, many=True)
        return Response(serializer.data)

    def post(self, request):
        aktyor=request.data
        serializer=AktyorSerializer(data=aktyor)
        if serializer.is_valid():
            data=serializer.validated_data
            Aktyor.objects.create(
                ism=data.get("ism"),
                davlat=data.get("davlat"),
                jins=data.get("jins"),
                tugilgan_yil=data.get("tugilgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class AktyorAPI(APIView):
    def get(self,request,son):
        aktyor=Aktyor.objects.get(id=son)
        serializer=AktyorSerializer(aktyor)

        return Response(serializer.data)

    def update(self,request,son):
        aktyor=Aktyor.objects.get(id=son)
        serializer=AktyorSerializer(aktyor, data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data
            Aktyor.objects.filter(id=son).update(
                ism=data.get("ism"),
                davlat=data.get("davlat"),
                jins=data.get("jins"),
                tugilgan_yil=data.get("tugilgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class KinolarAPI(APIView):
    def get(self,request):
        kinolar=Kino.objects.all()
        serializer=KinoSerializer(kinolar, many=True)
        return Response(serializer.data)

    def post(self,request):
        kino=request.data
        serializer=KinoQoshSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
