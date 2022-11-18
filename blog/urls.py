from django.urls import include, path, re_path
from rest_framework import routers

from blog import views

router = routers.DefaultRouter()
router.register(r'post', views.SnippetViewSet, basename='post')

urlpatterns = [path('', include(router.urls)),
               re_path('post/(?P<id>\d+)/comment', views.CommentsView.as_view(), name='comments'),
               ]
