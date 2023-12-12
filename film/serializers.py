from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import *

class AktyorSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    ism=serializers.CharField()
    davlat=serializers.CharField()
    jins=serializers.CharField()
    tugilgan_yil=serializers.DateField()

    # def validate(self, attrs):
    def validate_ism(self,qiymat):
        if len(qiymat)<4:
            raise  ValidationError("Ism, familiya juda qisqa")
        return qiymat

    def validate_jins(self,qiymat):
        if qiymat=='Erkak' or qiymat=='Ayol':
            return qiymat
        raise ValidationError("Jinsni noto'g'ri kiritingiz")


class KinoSerializer(serializers.ModelSerializer):
    aktyorlar=AktyorSerializer(many=True)
    class Meta:
        model=Kino
        fields='__all__'
    def to_representation(self, instance):
        kino=super(KinoSerializer,self).to_representation(instance)
        kino.update({"aktyorlar soni": len(kino.get("aktyorlar"))})
        kino.update({"izohlar soni": instance.izoh_set.all().count()})
        return kino

class KinoQoshSerializer(serializers.ModelSerializer):
    class Meta:
        model=Kino
        fields='__all__'
