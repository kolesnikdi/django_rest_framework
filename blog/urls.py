from django.urls import include, path
from rest_framework import routers

from blog import views

router = routers.DefaultRouter()
router.register(r'post', views.SnippetViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]
