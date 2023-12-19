from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import *
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.pagination import PageNumberPagination
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
        soz=request.query_params.get('ismi')
        davlati=request.query_params.get('davlati')
        tartib=request.query_params.get('order')
        if soz:
            aktyorlar=aktyorlar.filter(ism__contains=soz)
        if davlati:
            aktyorlar=aktyorlar.filter(davlat__contains=davlati)
        if tartib:
            aktyorlar=aktyorlar.order_by(tartib)
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

class IzohModelViewSet(ModelViewSet):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    order_fields = ['sana']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5


    # def perform_create(self, serializer):
    #     serializer.save()

    # def retrieve(self, request, *args, **kwargs):
    #     izoh=self.get_object()
    #     if izoh.baho<5:
    #         return Response
    #     return Response

class KinolarModelViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields=['id','nom', 'janr']
    order_fields=['id', 'janr']
    pagination_class = PageNumberPagination
    pagination_class.page_size=3

    def get_queryset(self):
        kinolar=self.queryset
        janr=self.request.query_params.get('janr')
        qidiruv=self.request.query_params.get("qidiruv")
        if qidiruv:
            kinolar=Kino.objects.annotate(oxshashlik=TrigramSimilarity('nom',qidiruv)
            ).filter(oxshashlik__gt=0.3).order_by('-oxshashlik')


        if janr:
            kinolar=kinolar.filter(janr__contains=janr)

        return kinolar
    # def list(self, request, *args, **kwargs):
    #     kinolar=self.queryset
    #     serializer=KinoSerializer(kinolar, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        kino=self.get_object()
        serializer=KinoSerializer(kino)
        return Response(serializer.data)

    @action(detail=True)
    def izohlar(self,request, pk):
        kino=self.get_object()
        kino_izohlari=kino.izoh_set.all()
        serializer=IzohSerializer(kino_izohlari, many=True)
        return Response(serializer.data)

class AktyorlarModelViewSet(ModelViewSet):
    queryset = Aktyor.objects.all()
    serializer_class = AktyorModelSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'ism', 'jins']
    order_fields = ['id', 'jins']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3

    def get_queryset(self):
        aktyorlar = self.queryset
        jins = self.request.query_params.get('jins')
        qidiruv = self.request.query_params.get("qidiruv")
        if qidiruv:
            aktyorlar = Aktyor.objects.annotate(oxshashlik=TrigramSimilarity('ism', qidiruv)
                                            ).filter(oxshashlik__gt=0.3).order_by('-oxshashlik')

        if jins:
            aktyorlar = aktyorlar.filter(jins__contains=jins)

        return aktyorlar
