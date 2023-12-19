from django.contrib import admin
from django.urls import path,include
from film.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("izohlar", IzohModelViewSet)
router.register("kinolarset", KinolarModelViewSet)
router.register("aktyorlarset", AktyorlarModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPI.as_view()),
    path('', include(router.urls)),
    path('aktyorlar/', AktyorlarAPI.as_view()),
    path('aktyor/<int:son>', AktyorAPI.as_view()),
    path('kinolar/', KinolarAPI.as_view()),
]
