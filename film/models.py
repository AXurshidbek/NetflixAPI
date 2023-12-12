from django.db import models
from django.contrib.auth.models import User

class Aktyor(models.Model):
    ism=models.CharField(max_length=35)
    davlat=models.CharField(max_length=25)
    jins=models.CharField(max_length=15)
    tugilgan_yil=models.DateField()

    def __str__(self):
        return self.ism

class Kino(models.Model):
    nom=models.CharField(max_length=35)
    janr=models.CharField(max_length=15)
    yil=models.DateField(blank=True,null=True)
    aktyorlar=models.ManyToManyField(Aktyor)

    def __str__(self):
        return self.nom

class Tarif(models.Model):
    nom=models.CharField(max_length=25)
    narx=models.PositiveIntegerField()
    davomiylik=models.DurationField()

    def __str__(self):
        return self.nom

class Izoh(models.Model):
    matn=models.TextField()
    sana=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    kino=models.ForeignKey(Kino,on_delete=models.CASCADE)
    baho=models.PositiveSmallIntegerField()

    def __str__(self):
        return self.matn